import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import pandas as pd
import re



def read_csv(path, debug):
  df = pd.read_csv(path)
  df = df[(df['Release Year']>=2010) & (df['Director'] != 'Unknown') & (df['Origin/Ethnicity'] == 'American')]

  if debug:
    df = df.head()
  return df

def spacy_tokeniser(String):
    String = String.lower().strip()
    processed_tokens = []
    tokens = nlp(String)
    for token in tokens:
        if (token.is_stop or token.is_punct):
            continue
        else:
            processed_tokens.append(token.lemma_)
    return processed_tokens

def process_genre(String):
  String = re.sub('sci-fi','science fiction',String)
  String = re.sub('bio-pic','biographical',String)
  String = re.sub('biopic','biographical',String)
  String = re.sub('-',' ', String)
  String = re.sub('/',' ', String)
  String = re.sub(',',' ', String)
  return String

def quantify_genre(String):
  String = process_genre(String)
  tokens = nlp(String)
  value = 0
  for token in tokens:
    if (token.is_stop is False):
      value += np.average(token.vector)
  return value

def get_indexes(links):
  # get indexes of all movies
  indexes = []
  for link in links:
    if link['source_idx'] not in indexes:
      indexes.append(link['source_idx'])

    if link['target_idx'] not in indexes:
      indexes.append(link['target_idx'])
  return indexes

def create_node_info(indexes, titles, genres):
  # get genre value for all movies
  nodes = []
  min_genre_value = 999
  max_genre_value = -999

  for i in indexes:
    genre_value = quantify_genre(genres[i])
    nodes.append({"id": titles[i], "genre": genres[i], "genre_value": genre_value})

    if genre_value < min_genre_value:
      min_genre_value = genre_value

    if genre_value > max_genre_value:
      max_genre_value = genre_value

  for n in nodes:
    # scale value to be between 0 and 180
    n['scaled_genre_value'] = int(((n['genre_value'] - min_genre_value) / (max_genre_value - min_genre_value))*180)
  return nodes

if __name__ == "__main__":
    nlp = spacy.load('en')
    debug=False

    # create df
    path = './wiki_movie_plots_deduped.csv'
    output_path = './data.json'
    df = read_csv(path, debug=debug)

    # compute tfidf matrix
    corpus = df['Plot'].values
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)

    L = len(df)
    similarity = cosine_similarity(X,X)
    titles = df['Title'].values

    # generate links
    links = []
    for i in range(L):
      for j in range(L):
        if (i < j) and similarity[i][j] >= 0.4:
            link = {}
            link['source_idx'] = i
            link['target_idx'] = j
            link['source'] = titles[i]
            link['target'] = titles[j]
            link['value'] = similarity[i][j]
            links.append(link)

    indexes = get_indexes(links)
    #indexes = [1,2,3,4,5]
    nodes = create_node_info(indexes, titles = df['Title'].values, genres = df['Genre'].values)

    # write to json file

    json_data = {"nodes" : nodes, "links" : links}
    with open(output_path, 'w') as outfile:
        json.dump(json_data, outfile)