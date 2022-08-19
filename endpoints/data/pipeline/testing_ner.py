### 
# Testing
###
nlp1 = spacy.load(r"C:\Users\jacoma\repos\coffee_app\output\model-best") #load the best model

content=[]
start=[]
end=[]
label=[]
for entry in validation_data:

    entities = entry[1]['entities']

    if len(entities) == 0:
        content.append(entry[0])
        start.append(-1)
        end.append(-1)
        label.append('NA')
    else:
        for entity in entities:
            content.append(entry[0])
            start.append(entity[0])
            end.append(entity[1])
            label.append(entity[2])

validationDF = pd.DataFrame({'content':content, 'start':start, 'end':end, 'label':label})

v_content=[]
v_text = []
v_start = []
v_end = []
v_label = []
for sent in pd.Series(content).unique():
    doc = nlp1(sent)

    spacy.displacy.serve(doc, style="ent")

    for ent in doc.ents:
        v_content.append(sent)
        v_text.append(ent.text)
        v_start.append(ent.start_char)
        v_end.append(ent.end_char)
        v_label.append(ent.label_)    

pred_valid_DF = pd.DataFrame({'content':v_content, 'text':v_text, 'start':v_start, 'end':v_end, 'label':v_label})

merged = pd.merge(validationDF, pred_valid_DF[['start', 'end', 'text', 'content', 'label']], how = "left", on = ['content', 'start', 'end'],  suffixes=['_valid', '_pred'])

merged[merged.label_valid != merged.label_pred]

#####
#
#####
def get_cleaned_label(label: str):
    if "-" in label:
        return label.split("-")[1]
    else:
        return label
    
    
def create_target_vector(doc):
    return [get_cleaned_label(label[2]) for label in doc[1]["entities"]]


def create_total_target_vector(docs):
    target_vector = []
    for doc in docs:
        target_vector.extend(create_target_vector(doc))
    return target_vector

#####
# Create Prediction Vector
#####
def create_prediction_vector(text):
    return [get_cleaned_label(prediction) for prediction in get_all_ner_predictions(text)]

    
def create_total_prediction_vector(docs: list):
    prediction_vector = []
    for doc in docs:
        prediction_vector.extend(create_prediction_vector(doc[0]))
    return prediction_vector

def get_all_ner_predictions(text):
    doc = nlp1(text)
    entities = [(e.start_char, e.end_char, e.label_) for e in doc.ents]
    
    return entities

#####
# Confusion Matrix
#####
from sklearn.metrics import confusion_matrix

def generate_confusion_matrix(docs): 
    classes = sorted(set(create_total_target_vector(docs)))
    y_true = create_total_target_vector(docs)
    predictions = create_total_prediction_vector(docs)

    y_pred = [pred[2] for pred in predictions]

    return confusion_matrix(y_true, y_pred)

generate_confusion_matrix(validation_data)

#####
# Calculate Evaluation Metrics
#####

#Precision

#Recall
