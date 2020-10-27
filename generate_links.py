import argparse
import json
import numpy as np
import pandas as pd
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

genre_mapping = {
    'biography/documentary': ['biography', 'documentary', 'biographical', 'historical', 'biopic'], 
    'action/adventure/thriller': ['action', 'superhero', 'disaster', 'crime', 'suspense', 'martial', 'adventure', 
                         'war', 'spy', 'epic', 'thriller'], 
    'comedy': ['comedy', 'parody', 'spoof'], 
    'drama': ['dramedy', 'drama', 'dramatic'], 
    'family': ['family', 'child', 'children'], 
    'sciencefiction/fantasy': ['fantasy', 'sci-fi', 'science-fiction', 'science fiction'], 
    'romance': ['romance', 'erotic', 'romantic'], 
    'musical': ['musical', 'dance'], 
    'horror/mystery': ['mystery', 'horror', 'slasher', 'supernatural', 'apocalyptic', 'dark'], 
    'animation': ['animation', 'anime', 'animated']
}

def define_genre_category(df):
    genres = df['Genre'].values
    
    genre_category = []
    
    for g in genres:
        movie_genre_category = []
        
        for m in genre_mapping:
            genre_word_list = genre_mapping[m]
            
            for w in genre_word_list:
                if w in g:
                    movie_genre_category.append(m)
                    break
        genre_category.append(movie_genre_category)
    return genre_category

    
def read_csv(path, debug):
  df = pd.read_csv(path)
  df = df[(df['Release Year']>=2010) & (df['Director'] != 'Unknown') & (df['Origin/Ethnicity'] == 'American')]

  if debug:
    df = df.head(30)
    
  genre_category = define_genre_category(df)
  
  df['genre_category'] = genre_category
  df = df[df.astype(str)['genre_category'] != '[]']
   
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

def shorten_plot(plots, num_sentences=3):
  short_plots = []
  for p in plots:
    sentences = p.split(".")
    short_plots.append(". ".join(sentences[:num_sentences]) + "...") 

  return short_plots

def create_node_info(indexes, titles, genre_categories, description):
  # get genre value for all movies
  nodes = []

  for i in indexes:
    nodes.append({"idx" : i,"id": titles[i], "genre": genre_categories[i], "description" : description})
  
  return nodes

def scale_similarity_value(x, similarity_threshold):
  c = 1 - (0.5/(1-similarity_threshold))
  scaled = (0.5/(1-similarity_threshold))*x + c
  assert scaled >= similarity_threshold
  assert int(scaled) <= 1
  return scaled

def main(args):
  debug = args['debug']
  if debug:
    print('In debug mode...')
  else:
    print('Not in debug mode...')

  nlp = spacy.load('en')

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
  if debug:
    similarity_threshold = 0.3
  else:
    similarity_threshold = 0.5

  links = []
  for i in range(L):
    for j in range(L):
      if (i < j) and similarity[i][j] >= similarity_threshold:
          link = {}
          link['source_idx'] = i
          link['target_idx'] = j
          link['source'] = titles[i]
          link['target'] = titles[j]
          link['value'] = scale_similarity_value(similarity[i][j], similarity_threshold)
          links.append(link)

  indexes = get_indexes(links)

  short_plots = shorten_plot(plots)
  
  nodes = create_node_info(indexes, titles = df['Title'].values, 
                            genre_categories = df['genre_category'].values,
                          description = short_plots)
  
  print(f'Number of links: {len(links)}')
  print(f'Number of nodes: {len(nodes)}')
  print(f'Saving data to {output_path}...')

  json_data = {"nodes" : nodes, "links" : links}
  with open(output_path, 'w') as outfile:
      json.dump(json_data, outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help = "Whether is in debug mode", default = False, required = False)
    args = vars(parser.parse_args())
    
    main(args)

    