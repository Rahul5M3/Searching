import spacy
from spacy import displacy
from spellchecker import SpellChecker
import pandas as pd
import os

import nltk
from nltk.corpus import words,stopwords

nltk.download('words')

word_list=set(words.words())
stop_words = set(stopwords.words('english'))

nlp = spacy.load("en_core_web_sm")

spell = SpellChecker()

def preprocess_text(text):
    doc = nlp(text)
    processed_text=[]
    c_words=[]

    for token in doc:
        c_words.append(token.text)

    for token in doc:
        if token.text==spell.correction(token.text):
            words=spell.candidates(token.text)
            valid_words={word for word in words if word in word_list and word not in stop_words}
            v_words=" ".join(words)
            for t in nlp(v_words):
                if not t.is_stop and not t.is_punct and t.has_vector:
                    c_words.append(t.text)
            processed_text.append(valid_words)    
    return c_words

def extract_entities(text):
    entities=[]
    doc=nlp(text)
    for ent in doc.ents:
        entities.append(ent.text)
    return entities     

def extracting_data_from_csv(words,csv):
    try:
        df=pd.read_csv(csv)
        mask=df.apply(lambda row : row.astype(str).str.contains('|'.join(words), case=False).any(), axis=1)   
        filtered_data=df[mask]
        filtered_data.to_json('data/filtered_data_result.json', orient='records')
    except Exception as e :
         print(f"Error: The file was not found.{e}")    

# text="Elon Musk, the CEO of SpaceX, announced in a press conference in Los Angeles that the company will be launching a new spacecraft next year. The spacecraft, named 'Falcon Star,' aims to explore Mars and beyond. According to Musk, this project is a significant step toward humanity's goal of colonizing the Red Planet. The event was covered by major media outlets, including The New York Times and BBC News."

# textProcessing=preprocess_text(text)
# print(textProcessing)

# entitiesProcessing=" ".join(textProcessing)
# entities=extract_entities(entitiesProcessing)
# print(entities)
