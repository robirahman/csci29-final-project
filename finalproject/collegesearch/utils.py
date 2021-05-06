from numpy import log, abs
from numpy import dot, zeros, ones, add
from numpy.linalg import norm as mag
import pandas as pd
import re
from functools import reduce


def cosine_similarity(a, b):
    similarity = dot(a, b) / (mag(a) * mag(b))
    return similarity

def get_colleges():
    college_info = pd.read_csv("finalproject/collegesearch/college_data/facts.csv")
    college_embeddings = pd.read_csv("finalproject/collegesearch/college_data/embedding.csv")
    vectors = [row[1][1:] for row in college_embeddings.iterrows()]
    college_info["description"] = vectors
    return [row[1] for row in college_info.iterrows()]

def score_all_colleges(preferences):
    colleges = get_colleges()
    for college in colleges:
        college["score"] = calculate_match(preferences, college)
    return colleges

def top_matches(preferences):
    colleges = score_all_colleges(preferences)
    return sorted(colleges, key = lambda i: i["score"], reverse=True)[0:10]

def embed_description(description: str):
    if description == "":
        return ""
    else:
        embedding_df = pd.read_csv("finalproject/collegesearch/college_data/embedding_dict.csv")
        embedding = WordEmbedding(embedding_df)
        try:
            description_vector = embedding.embed_document(description).values
        except AttributeError:
            description_vector = ones(100)
        return description_vector

def calculate_match(preferences, college_info):
    score = 35

    # Describe the college you want to go to.
    if preferences["vector"] == "":
        score += 25
    else:
        similarity = cosine_similarity(preferences["vector"], college_info["description"])
        score += 25 * similarity

    # How many undergraduates should the college have?
    x = preferences["size"]
    y = college_info["size"]
    size_match = 1-(abs(log(x/y)))
    score += 10 * size_match

    # User's SAT scores
    sat = preferences["sat_verbal"] + preferences["sat_math"]
    if sat < college_info["sat_min"]:
        score += (sat - college_info["sat_min"])/40
    if sat < college_info["sat_max"]:
        score += (sat - college_info["sat_max"])/40

    # College's ranking
    score += (100-college_info[0])/5

    # Tuition
    price = int(re.sub('\D','',college_info["price"]))
    score += -price/5000

    # Do you prefer public colleges, private colleges, or neither?
    if preferences["public"] == 2:
        score += 0
    elif preferences["public"] == college_info["public"]:
        score += 10
    elif preferences["public"] != college_info["public"]:
        score += -10

    return score



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
        default = zeros(
            100,
        )
        # getting a map of the dictionary vectors
        vec = map(lambda t: self.dict.get(t, default), tokenized)
        # reducing the matrixes via
        averaged_vec = reduce(lambda x, y: x + y, vec)
        return averaged_vec