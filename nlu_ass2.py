# -*- coding: utf-8 -*-
"""NLU_ASS2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BuMUkE0iPEufPD5XC35H4bIqweGmwk7Q

## PART A
"""

import tensorflow as tf
import json
import string
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import numpy as np
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

# Load the data from the file and preprocess it
data = []
for line in open('train.json', 'r'):
    data.append(json.loads(line))

# Define the class of relations to classify
relations_to_classify = ["CEO",'SUBSIDIARY_OF','DATE_OF_DEATH','RESIDENCE', 'BIRTH_PLACE', 'NATIONALITY', 'EMPLOYEE_OR_MEMBER_OF', 'EDUCATED_AT', 'POLITICAL_AFF', "CHILD_OF", 'SPOUSE', "DATE_FOUNDED", 'HEADQUARTERS', 'FOUNDED_BY']

def preprocess_text(text):
    """
    This function performs basic text preprocessing by removing punctuations, 
    converting text to lowercase, and removing extra white spaces.
    """
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub('\s+', ' ', text)
    text = text.lower().strip()
    return text

# Modify preprocess_data to return a list of relations for each passage
def preprocess_data(data):
    """
    This function preprocesses the Knowledgent dataset by extracting the 
    document text and the annotated properties for each passage. It also 
    performs text preprocessing on the document text.
    """
    X = []
    y = []
    for d in data:
        document_text = d['documentText']
        document_text = preprocess_text(document_text)
        for passage in d['passages']:
            passage_text = passage['passageText']
            passage_text = preprocess_text(passage_text)
            annotated_properties = []
            for fact in passage['exhaustivelyAnnotatedProperties']:
                annotated_properties.append(fact['propertyName'])
            # Filter for only the desired relations
            if any(prop in relations_to_classify for prop in annotated_properties):
                X.append(passage_text)
                # Convert the list of annotated properties to binary labels
                y.append([prop for prop in annotated_properties if prop in relations_to_classify])
    return X, y

# Modify the prediction function to output the relation(s) instead of binary labels
def predict_relation(model, text):
    """
    This function takes a trained model and an input text, preprocesses the text,
    and returns the predicted relation(s) for the input text.
    """
    text = preprocess_text(text)
    text_bow = vectorizer.transform([text]).toarray()
    prediction = model.predict(text_bow)[0]
    # Convert the prediction to binary labels
    binary_prediction = [1 if p > 0.5 else 0 for p in prediction]
    # Use relations_to_classify to determine the predicted relation(s)
    predicted_relations = [relations_to_classify[i] for i, label in enumerate(binary_prediction) if label == 1]
    return predicted_relations


X, y = preprocess_data(data)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Extract bag-of-words features from the text data
vectorizer = CountVectorizer()
X_train_bow = vectorizer.fit_transform(X_train)
X_test_bow = vectorizer.transform(X_test)
import numpy as np



# Define the model architecture
model = Sequential([
    Dense(512, activation='relu', input_shape=(X_train_bow.shape[1],)),
    Dropout(0.5),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(14, activation='sigmoid') # modified last layer
])

# Compile the model
optimizer = Adam(learning_rate=0.001)
model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# Train the model
# Train the model
from sklearn.preprocessing import MultiLabelBinarizer

# Convert the lists of lists to binary labels
mlb = MultiLabelBinarizer(classes=relations_to_classify)
y_train = mlb.fit_transform(y_train)
y_test = mlb.transform(y_test)

# Train the model
history = model.fit(X_train_bow.toarray(), y_train, epochs=10, batch_size=32, validation_data=(X_test_bow.toarray(), y_test))

"""PART B"""

def preprocess_data(data):
    """
    This function preprocesses the Knowledgent dataset by extracting the 
    document text and the annotated properties for each passage. It also 
    performs text preprocessing on the document text. It only appends passages
    that contain the desired relations.
    """
    X = []
    y = []
    for d in data:
        document_text = d['documentText']
        document_text = preprocess_text(document_text)
        for passage in d['passages']:
            passage_text = passage['passageText']
            passage_text = preprocess_text(passage_text)
            annotated_properties = []
            for fact in passage['exhaustivelyAnnotatedProperties']:
                annotated_properties.append(fact['propertyName'])
            # Filter for only the desired relations
            if any(prop in ["DATE_OF_BIRTH", "PLACE_OF_RESIDENCE", "BIRTHPLACE", "NATIONALITY", "EMPLOYEE_OR_MEMBER_OF", "EDUCATED_AT"] for prop in annotated_properties):
                X.append(d)
                # Convert the list of annotated properties to binary labels
                y.append([prop for prop in annotated_properties if prop in relations_to_classify])
    return X, y

p,r=preprocess_data(data)
p

"""# Used to find information about nodes and relationships to create KG in neo4j"""

desired_relations = ["12",'11','10','15','3','9']
extracted_facts = []

for data_point in data:
    for passage in data_point["passages"]:
        for fact in passage["facts"]:
            if fact["propertyId"] in desired_relations:
                extracted_facts.append(fact)
                

human_readable_list = []
for item in extracted_facts:
    human_readable_list.append(item['humanReadable'])
    human_readable_list.append('para_end')

human_readable_list
