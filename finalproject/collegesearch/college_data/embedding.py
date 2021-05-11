import re
from functools import reduce
import bs4 as BeautifulSoup
import pandas as pd
import codecs
import wikipedia
from gensim.models import Word2Vec
import requests
import numpy as np

class WordEmbedding(object):
    def __init__(self, dict):
        # feeding words and vecs into a dictionary via zip.
        self.dict = dict

    def __call__(self, word):
        """Embed a word

        :returns: vector, or None if the word is outside of the vocabulary
        :rtype: ndarray
        """
        # Consider how you implement the vocab lookup.  It should be O(1).
        return self.dict.get(word, None)

    @classmethod
    def tokenize(self, text):
        """Get all "words", including contractions

        Example::

            tokenize("Hello, I'm Scott") --> ['hello', "i'm", 'scott']
        :returns: list of words in statement.
        :rtype: list
        """
        return re.findall(r"\w[\w']+", text.lower())

    def cos_sim(self, reference, reference2):
        """Get cosine similarity for two matrixes

        :returns: cosign simularity
        :rtype: int
        """
        # get dot product of the arrays
        numerator = np.dot(reference2, reference)
        # multiply vectors normalizatized
        dominator = np.linalg.norm(reference2) * np.linalg.norm(reference)
        return numerator / dominator

    def embed_document(self, text):
        """Convert text to vector, by finding vectors for each word and combining

        :param str document: the document (one or more words) to get a vector
            representation for

        :return: vector representation of document
        :rtype: ndarray (1D)
        """
        # Use tokenize(), maybe map(), functools.reduce, itertools.aggregate...
        # Assume any words not in the vocabulary are treated as 0's
        # Return a zero vector even if no words in the document are part
        # of the vocabulary
        tokenized = self.tokenize(text)
        # setting 0 vector
        # fmt: off
        default = np.zeros(300,)
        # fmt: on
        # getting a map of the dictionary vectors
        vec = map(lambda t: self.dict.get(t, default), tokenized)
        # reducing the matrixes via
        averaged_vec = reduce(lambda x, y: x + y, vec)
        return averaged_vec
def create_dict(wiki_list, bypass):
    """creates dictionary for the embedding class used in pset 3

        :returns: vector/word dictionary.
        :rtype: df
    """
    if bypass:
        return pd.read_csv('college_data/embedding_dict.csv')
    wiki_list = wiki_list['wiki'].to_list()
    #tokenize wikipedia pages
    tokenized_sentences = np.array(list(map(WordEmbedding.tokenize, wiki_list)))
    #feed into word2vec model
    model = Word2Vec(tokenized_sentences, window=2, min_count=0, vector_size=100, workers=4)
    words = model.wv.key_to_index
    we_dict = {word: model.wv[word] for word in words}
    #obtain words and vectors from word2vec
    return pd.DataFrame(data=we_dict)
def college_embeddings(we_dict, wiki_list, facts, bypass):
    """embeds the colleges with the pset 3 wordembeddings class using word2vec dictionary

        :returns: vectors for colleges.
        :rtype: df
    """
    if bypass:
        return pd.read_csv('college_data/college_embeddings.csv')
    names = facts['names'].to_list()
    wiki_list = wiki_list['wiki'].to_list()
    tokenized_sentences = np.array(list(map(WordEmbedding.tokenize, wiki_list)))
    model = Word2Vec(tokenized_sentences, window=2, min_count=0, vector_size=100, workers=4)
    words = model.wv.key_to_index
    we_dict = {word: model.wv[word] for word in words}
    #basically, feed it into pset 3 stuff, no explain needed
    embedding = WordEmbedding(we_dict)
    embeddings = np.array(list(map(embedding.embed_document, wiki_list)))
    college_embedding = pd.DataFrame(embeddings, names)
    return college_embedding

def create_wiki(facts, bypass):
    """obtains the wikipedia pages of the colleges

        :returns: wikipedia pages
        :rtype: dict
    """
    if  bypass:
        return pd.read_csv('college_data/wiki_list.csv')
    #grab names of colleges
        names = facts['names'].to_list()
        wiki_list = []
        for search in names:
            #search wikipedia
            wiki = wikipedia.page(search).content
            #save wikipedia page text in list
            wiki_list.append(wiki)
        data = {'wiki': wiki_list}
        wiki_list = pd.DataFrame(data=data)
        return wiki_list

def college_facts(bypass):
    """gets the facts about the colleges from niche html file, as well as the collegescore api.

        :returns: college facts
        :rtype: df
    """
    #bypass arg, if true then task is skipped.
    if bypass:
        return pd.read_csv('college_data/college_data.csv')
    #load html file with codecs
    html = codecs.open("college_data/niche_college_list_1.html")
    #load object into beautifulsoup
    soup = BeautifulSoup(html, "html.parser")
    #create fact lists
    names = []
    attend = []
    price = []
    sat_min = []
    sat_max = []
    wiki_list = []
    state = []
    size = []
    #using beautiful soup grab college fact data from the niche html file
    for x in soup.select(".card"):
        if x.find(string="Sponsored") is None:
            for y in x.select(".search-result__title"):
                name = y.text
                names.append(name)
                if name == "William & Mary":
                    name = "College of William & Mary"
                #also grab student body size and state from collegescorecard api
                gov_api = requests.get(
                    "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.name="
                    + name
                    + "&fields=id,school.name,school.state,2018.student.size&api_key=iaXf7WP3wErOgNGAQRBblY905k4JDfHmeDSYBpcR"
                ).json()
                #data cleaning
                if search == "Northwestern University":
                    search = "north western university"
                elif search == "Bowdoin College":
                    search = "bowden college"
                elif search == "Williams College":
                    search = "william college"
                elif search == "Northeastern University":
                    search = "north western university"
                elif search == "Kenyon College":
                    search = "kenyan college"
                if name == "College of William & Mary":
                    size.append(6300)
                    state.append("VA")
                elif name == "Massachusetts Institute of Technology":
                    size.append(4500)
                    state.append("MA")
                elif name == "Harvard University":
                    size.append(6755)
                    state.append("MA")
                elif name == "Washington University in St. Louis":
                    size.append(7356)
                    state.append("WA")
                elif name == "Colby College":
                    size.append(2000)
                    state.append("ME")
                elif name == "Washington & Lee University":
                    size.append(1822)
                    state.append("VA")
                elif name == "The Cooper Union for the Advancement of Science and Art":
                    size.append(845)
                    state.append("NY")
                elif name == "Texas A&M University":
                    size.append(56205)
                    state.append("TX")
                elif name == "The Ohio State University":
                    size.append(46984)
                    state.append("OH")
                elif name == "Cornell University":
                    size.append(15105)
                    state.append("NY")
                elif name == "University of Chicago":
                    size.append(6600)
                    state.append("IL")
                else:
                    size.append(gov_api["results"][0]["2018.student.size"])
                    state.append(gov_api["results"][0]["school.state"])
            for z in x.select(".search-result-fact"):
                for q in z.select(".search-result-fact__label"):
                    for w in z.select(".search-result-fact__value"):
                        if q.text == "Acceptance Rate":
                            attend.append(w.text)
                        if q.text == "Net Price":
                            price.append(w.text)
                        if q.text == "SAT Range":
                            sat_min.append(w.text[0:4])
                            sat_max.append(w.text[-4:])
                for z in x.select(".search-result-fact"):
                    for q in z.select(".search-result-fact__label"):
                        for w in z.select(".search-result-fact__value"):
                            if q.text == "Acceptance Rate":
                                attend.append(w.text)
                            if q.text == "Net Price":
                                price.append(w.text)
                            if q.text == "SAT Range":
                                sat_min.append(w.text[0:4])
                                sat_max.append(w.text[-4:])
        data = {'sat_min': sat_min, 'sat_max': sat_max, 'names': names, 'price': price, 'acceptance': attend,
                'size': size}
        college_facts = pd.DataFrame(data=data)
        return college_facts


