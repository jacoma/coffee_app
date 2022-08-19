#######
# ARCHIVE
#######
import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

tokenizer = RegexpTokenizer(r'\w+')
lemmatizer = WordNetLemmatizer()

for i in range(0, len(new_coffee)):
    if type(new_coffee.loc[i, 'roaster_notes'])==float:
        new_coffee.loc[i, 'roaster_notes']=''   

new_coffee['all_notes'] = new_coffee['other_notes']+' '+(new_coffee['roaster_notes'])

notes_3 = all_notes.Note_3

temp_df=pd.DataFrame(columns=['product_id', 'notes_list'])
for i in range(0,len(new_coffee)):
    print(i)

    notes_list = []

    tokens = tokenizer.tokenize(new_coffee.loc[i, 'all_notes'])
    filtered_tokens = [t.lower() for t in tokens if not t in stopwords.words("english")]
    lem_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    token_list = []
    for token in lem_tokens:
        result = list(words_in_string(notes_3, token))

        if len(result) > 0:
            token_list.append(result)

    combined_text = ' '.join(lem_tokens)
    ngram_object = TextBlob(combined_text)
    ngrams = ngram_object.ngrams(n=2) # Computing Bigrams

    for ngram in ngrams:
        text = ' '.join(ngram)
        result = list(words_in_string(notes_3, text))

        if len(result) > 0:
            token_list.append(result)

    for t in token_list:
        notes_list.extend(t)

    notes_set = set(notes_list)
    
    new_row = {'product_id': new_coffee.product_id[i], 'notes_list':",".join(notes_set)}
    
    temp_df = temp_df.append(new_row, ignore_index=True)

trade_notes_df = pd.merge(new_coffee, temp_df, how='inner', on='product_id')