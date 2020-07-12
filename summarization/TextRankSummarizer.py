import numpy as np
import pandas as pd

import re

import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

from sklearn.metrics.pairwise import cosine_similarity

import networkx as nx


def _clean_text(df, columnn='text'):
    """Note that this is customized for this particular dataset, will need to think of how this should be constructed once we get the actual data.

    This particular file has some formatting issues so I need to add spaces and remove instances of \n to get the sentences tokenized properly."""

    df[columnn] = df[columnn].str.replace('\n', '')
    df[columnn] = df[columnn].str.replace('.', '. ')
    df[columnn] = df[columnn].str.replace('.  ', '. ')
    df[columnn] = df[columnn].str.replace('?', '? ')
    df[columnn] = df[columnn].str.replace('!', '! ')
    df[columnn] = df[columnn].str.replace(':', ': ')

    return df


def _make_tokens(df, column='text', row=0):
    """This will create a list where each item is a sentence from the dataframe.
    
    By default, it will only grab sentences from the first row, but row can be specified.
    
    To do: create dictionary / dataset with key value pairs of documents and sentences, so every sentence in an entire dataset is included."""

    _sentences = []
    df = df.iloc[[row]]
    for s in df[column]:
	    _sentences.append(sent_tokenize(s))

    _sentences = [y for x in _sentences for y in x]

    return _sentences


def _load_embeddings():

    """
    This function will create a dictionary of GloVe word embeddings to be used later.
    
    downloading pre-trained GloVe word embeddings (trained on Wikipedia articles) from:
    
    http://nlp.stanford.edu/data/glove.6B.zip
    """

    word_embeddings = {}
    f = open('data/glove.6B/glove.6B.100d.txt', encoding='utf-8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()

    return word_embeddings


# function to remove stopwords (CHECK THIS IS FUNCTION ISN"T WORKING)
def _remove_stopwords(sen):
    stop_words = stopwords.words('english')
    sen_new = " ".join([i for i in sen if i not in stop_words])
    
    return sen_new

def _process_text(_sentences):

    _clean_sentences = pd.Series(_sentences).str.replace("[^a-zA-Z]", " ")
    _clean_sentences = [s.lower() for s in _clean_sentences]
    
    _clean_sentences = [_remove_stopwords(r.split()) for r in _clean_sentences]

    return _clean_sentences



def _make_sentence_vectors(_clean_sentences, word_embeddings):

    _sentence_vectors = []

    for i in _clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((100,))
        _sentence_vectors.append(v)    

    return _sentence_vectors


def _find_similarities(_clean_sentences, _sentence_vectors):

    """This will first initiate a similarity matrix, and then populate it with the cosine similarity values from the sentence vectors"""

    _sim_mat = np.zeros([len(_clean_sentences), len(_clean_sentences)])

    for i in range(len(_clean_sentences)):
        for j in range(len(_clean_sentences)):
            if i != j:
                _sim_mat[i][j] = cosine_similarity(_sentence_vectors[i].reshape(1,100), _sentence_vectors[j].reshape(1,100))[0,0] 

    return _sim_mat




def _rank_sentences(_sim_mat, _sentences):
    """This function will rank each sentence based on its relative importance given by the textrank/pagerank.
    It converts the similarity matrix into a graph where each node is a sentence, and each edge is the corresponding similarity vector to each other sentence.
    The pagerank algorithm then scores each sentence on how important it is to the network of sentences.
    For more info on PageRank, see here: https://en.wikipedia.org/wiki/PageRank"""

    nx_graph = nx.from_numpy_array(_sim_mat)
    scores = nx.pagerank(nx_graph)

    _ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(_sentences)), reverse=True)

    return _ranked_sentences


def get_summary(df, column='text', row=0, sentence_length=5):

    _clean_text(df, column)

    _sentences = _make_tokens(df, column, row)

    word_embeddings = _load_embeddings()

    _clean_sentences = _process_text(_sentences)

    _sentence_vectors = _make_sentence_vectors(_clean_sentences, word_embeddings)
    _sim_mat = _find_similarities(_clean_sentences, _sentence_vectors)

    _ranked_sentences = _rank_sentences(_sim_mat, _sentences)

    final_summary = []

    for i in range(sentence_length):
        summary_sentence = _ranked_sentences[i][1]
        final_summary.append(summary_sentence)
    
    return final_summary



# # %%
# df = pd.read_csv("data/medium_articles.csv")

# get_summary(df)

# # %%
# get_summary(df, row=1)

# # %%
