import re
from functools import reduce

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
