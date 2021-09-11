import pandas as pd
import numpy as np
import os
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from endpoints.ml.postgres_data import get_postgres_data, create_postgres_data
from azure.storage.blob import BlockBlobService
from io import StringIO
from scipy.spatial.distance import pdist, squareform
from coffee.models import recommendations, dim_coffee
from django.db.models import Max, F

lemmatizer = WordNetLemmatizer()


class Recommendations:
    def __init__(self):
        print("Recommender Loaded")

    def get_recs(self, user):
        user_recs=recommendations.objects.filter(user_id=user.id)
        max_set = user_recs.aggregate(max=Max('recs_set'))

        if max_set:
            latest_recs=user_recs.filter(recs_set=max_set['max'])
        else:
            latest_recs=user_recs

        rec_list = latest_recs.values_list('coffee_id', flat=False).distinct()

        context = dim_coffee.objects.filter(coffee_id__in = rec_list)
        return context


    def create_recs(self, user, new_rating=None):
        #get data
        notes, coffee_df, all_notes, ratings = self.get_data(user)
        notes_3 = all_notes.Note_3

        if not new_rating==None:
            ratings.append(new_rating, ignore_index=True)

        #get clean notes
        clean_notes = self.get_clean_notes(coffee_df, notes_3)

        complete_info = pd.merge(clean_notes, all_notes, how='left', left_on='cleaned_note', right_on='Note_3')

        #get jaccard
        jaccard = self.get_jaccard_scores(complete_info)

        #get recs
        recs = self.top_recs(ratings, jaccard, user.id)

        latest_set = get_postgres_data(f'SELECT COALESCE(MAX(recs_set), 0) FROM coffee_recommendations WHERE user_id_id={user.id}')
        new_set = latest_set+1
        
        for i in range(0, len(recs)):
            coffee_x = dim_coffee.objects.get(coffee_id = recs.iloc[i, 2])
            
            rec = recommendations(
                user_id = user,
                rec_num = i,
                coffee = coffee_x,
                score = recs.iloc[i, 3],
                recs_set_num=new_set
            )

            rec.save()

        return print("New recommendations saved")


    def get_data(self, user):
        notes = get_postgres_data('SELECT * FROM coffee_dim_notes')

        ratings = get_postgres_data(f'SELECT rating, coffee_id, user_id_id FROM coffee_ratings WHERE user_id_id={user.id}')

        coffee_df = get_postgres_data('SELECT * FROM coffees')

        notes_coffee_df = coffee_df[['coffee_id', 'notes']]
        notes_noNA_coffee_df = notes_coffee_df.dropna()
        
        blob_service = BlockBlobService( 
            account_name=os.getenv('AZ_STORAGE_NAME', None), 
            account_key=os.getenv('AZURE_ACCOUNT_KEY', None))

        blob_string = blob_service.get_blob_to_text('coffeecontainer', 'notes_wheel.csv')
        all_notes = pd.read_csv(StringIO(blob_string.content))

        return notes, notes_noNA_coffee_df, all_notes, ratings

    def get_clean_notes(self, coffee_df, notes):
        matched_notes_df = self.match_notes(coffee_df, 0, 1, notes)

        temp_df = matched_notes_df.notes_list.str.split(',', expand=True)

        coffee_notes_df = pd.concat([matched_notes_df, temp_df], axis=1)

        coffee_melt_df = pd.melt(
            coffee_notes_df, 
            id_vars='coffee_id', 
            value_vars=list(range(0, len(temp_df.columns), 1)),
            var_name='note_num',
            value_name='cleaned_note'
        )

        clean_notes = coffee_melt_df[coffee_melt_df['cleaned_note'].isna()==False]
        
        return clean_notes

    def get_jaccard_scores(self, df):
        ##****** JACCARD SIMILARITY ******##
        unique_notes = df.Note_2

        dum_df = pd.get_dummies(unique_notes)

        new_df = df.drop('Note_2', axis=1)
        newnew_df = new_df.join(dum_df)

        grouped_df = newnew_df.groupby('coffee_id')

        sum_df = grouped_df.sum()

        j_scores_df = self.calculate_jaccard(sum_df)

        return j_scores_df


    def words_in_string(self, word_list, a_string):
        '''Returns unique elements found in both lists'''
        my_list = [] 
        split_list = a_string.split()
        for elem in split_list:
            my_list.append(elem)
        my_list.append(a_string)
        return set(word_list).intersection(my_list)

    def match_notes(self, df, id_col, notes_col, notes_wheel_list):
        temp_df=pd.DataFrame(columns=['coffee_id', 'notes_list'])
        for i in range(0, len(df)):
            tok_split = df.iloc[i, notes_col].split(',')

            notes_list = []
            for tok in tok_split:
                tok_list = []
                tokens = [token.lower() for token in word_tokenize(tok)]
                lemmatized_words = [lemmatizer.lemmatize(token) for token in tokens]
                lem = ' '.join(lemmatized_words)

                tok_list.append(list(self.words_in_string(notes_wheel_list, lem)))
                # tok_list.append(list(words_in_string(notes_2, lem)))

                for tok in tok_list:
                    notes_list.extend(tok)
        
            new_row = {'coffee_id': df.iloc[i, id_col], 'notes_list':",".join(notes_list)}
        
            temp_df = temp_df.append(new_row, ignore_index=True)

        return temp_df

    def calculate_jaccard(self, df):
         # Find jaccard score for each coffee compared to all other coffees
        jaccard_distances = pdist(df.values, metric='jaccard')

        # Convert the distances to a square matrix
        jaccard_similarity_array = 1 - squareform(jaccard_distances)

        # Wrap the array in a pandas DataFrame
        jaccard_df = pd.DataFrame(jaccard_similarity_array, index=df.index, columns=df.index)

        jaccard_df = jaccard_df.reset_index()

        # Melt the dataframe to convert each coffee column into a coffee row.
        jaccard_melt_df = pd.melt(
            jaccard_df, 
            id_vars='coffee_id', 
            var_name='coffee',
            value_name='jaccard'
        )

        jaccard_melt_df = jaccard_melt_df[ (jaccard_melt_df.coffee_id != jaccard_melt_df.coffee)]

        return jaccard_melt_df


    def top_recs(self, rate_df, jaccard_df, user_id):
        top_rated = rate_df[(rate_df['rating']>=5) & (rate_df['user_id_id'] == user_id)].coffee_id.unique()

        my_recs = jaccard_df[jaccard_df['coffee_id'].isin(top_rated) & (jaccard_df.jaccard!=0) & ~jaccard_df['coffee'].isin(rate_df.coffee_id.unique())].sort_values(['coffee_id', 'jaccard'], ascending=False)

        final_recs = my_recs.sort_values(['jaccard'], ascending=False).head(5)
        final_recs = final_recs.reset_index()

        return final_recs 

    