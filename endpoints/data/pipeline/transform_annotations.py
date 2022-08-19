import json
import random

file_path = "C:\\Users\\jacoma\\Downloads\\coffee-batch_annotations.json"

f = open(file_path, encoding='utf8')

data = json.load(f)

complete_data = []
for i,row in enumerate(data['examples']):
    content = row['content']
   
    entityList = []
    for i,row in enumerate(row['annotations']):
        start = row['start']
        end = row['end']
        entity = row['tag']

        annote = (start, end, entity)

        entityList.append(annote)

    entityDict = {}
    entityDict['entities'] = entityList

    complete_data.append((content, entityDict))

random.seed(325)
idx = random.sample(range(0, len(complete_data)), 145, )

training_data=[complete_data[i] for i in idx]

nontraining_data=[complete_data[i] for i in range(0, 244) if i not in idx]

validation_data=nontraining_data[0:50]

test_data=nontraining_data[50:100]


#####
# CONVERT TO .spacy FORMAT
#####
import pandas as pd
import os
from tqdm import tqdm ###progress meter for for loops.
import spacy
from spacy.tokens import DocBin

def create_spacy_format(data):
    nlp = spacy.load("en_core_web_sm")

    db = DocBin() # create a DocBin object

    for text, annot in tqdm(data): # data in previous format
        doc = nlp.make_doc(text) # create doc object from text

        ents = []
        for start, end, label in annot["entities"]: # add character indexes
            span = doc.char_span(start, end, label=label, alignment_mode="contract")

            if span is None:
                print("Skipping entity")
            else:
                ents.append(span)

        doc.ents = ents # label the text with the ents

        db.add(doc)
    
    return db

training_db = create_spacy_format(training_data)
validation_db = create_spacy_format(validation_data)
test_db = create_spacy_format(test_data)

training_db.to_disk('endpoints\\data\\tmp\\train.spacy') 
validation_db.to_disk('endpoints\\data\\tmp\\validation.spacy') 
test_db.to_disk('endpoints\\data\\tmp\\test.spacy') 