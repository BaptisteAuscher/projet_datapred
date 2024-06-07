import requests
import pandas as pd

from dotenv import load_dotenv
load_dotenv()
import os

HUGGING_FACE_API = os.getenv('HUGGING_FACE_API')

API_URL_SUMMERIZATION = "https://api-inference.huggingface.co/models/Falconsai/text_summarization"

API_URL_FEELING_ANALYSIS = "https://api-inference.huggingface.co/models/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
headers = {"Authorization": f"Bearer {HUGGING_FACE_API}"}

def query(payload, API_URL):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

sorted_corpus = {}
	
def sort_corpus_by(keywords) :
    """
    Create a csv file for each list of keyword in keywords, containing all articles from corpus 
    with the words from the list in them
    Example : [["france", "EDF"], ["england"], ["russia"]] gives you :
              .... corpus_france_EDF.csv                                
              ....... corpus_england.csv
              ........ corpus_russia.csv
    """
    corpus = pd.read_csv("../big_corpus.csv")
    colonnes = [
        'uri', 'lang', 'isDuplicate', 'date', 'time', 'dateTime', 'dateTimePub',
        'dataType', 'sim', 'url', 'title', 'body', 'source_uri', 'source_dataType',
        'source_title', 'authors', 'sentiment', 'wgt', 'relevance', 'image', 'eventUri'
    ]
    sorted_corpus_kw = {"_".join(keyword): pd.DataFrame(columns=colonnes) for keyword in keywords}
    
    df_iterrows = corpus.iterrows()
    for index, row in df_iterrows :
        for keyword in keywords :
            flag = 1
            for each_keyword in keyword :
                if each_keyword not in row['body'] :
                    flag *= 0
            if flag == 1 :
                sorted_corpus_kw["_".join(keyword)] = pd.concat([sorted_corpus_kw["_".join(keyword)], row.to_frame().T], ignore_index=True)
    sorted_corpus.update(sorted_corpus_kw)


sort_corpus_by([["france", "gas"]])
size = len(sorted_corpus["france_gas"])
articles = sorted_corpus["france_gas"]["body"].tolist()
for i in range(min(size,5)):
    print(query({"inputs": articles[i],"parameters": {"max_length": 2000, "min_length":500, "do_sample":False}}, API_URL_SUMMERIZATION))

#hello world

b90b828e355000bfd8674ed967554f3603e3f3b5