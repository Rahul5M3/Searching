import pandas as pd
import json
import sys
from utils import preprocess_text, extract_entities, extracting_data_from_csv

def search(query):
    query=preprocess_text(query)
    entities=extract_entities(" ".join(query))
    if len(entities)> 0 :
        extracting_data_from_csv(entities,'data/data.csv')

if __name__=="__main__":
    if len(sys.argv) > 1 :
        search(sys.argv[1])


# search("Emma Martin india")        