from numpy import log, abs
from numpy import dot, zeros, ones, add
from numpy.linalg import norm as mag
import pandas as pd
import re
from functools import reduce, partial
from typing import List, Dict


def cosine_similarity(a, b) -> float:
    """Calculates the angle between two vectors. If used on two word embedding
    vectors, the effect is to return the similarity of their texts."""
    similarity = dot(a, b) / (mag(a) * mag(b))
    return similarity


def get_colleges() -> List[Dict]:
    college_info = pd.read_csv("finalproject/collegesearch/college_data/facts.csv")
    college_embeddings = pd.read_csv(
        "finalproject/collegesearch/college_data/embedding.csv"
    )
    vectors = [row[1][1:] for row in college_embeddings.iterrows()]
    college_info["description"] = vectors
    return [row[1] for row in college_info.iterrows()]


def score_all_colleges(preferences: List[Dict]) -> List[Dict]:
    """Calls a partial() evaluation of calculate_match() to bind
    the submitted list of preferences. The resulting partial function
    is then used to associate a score with every college."""
    colleges = get_colleges()
    score = partial(calculate_match, preferences=preferences)
    for college in colleges:
        college["score"] = score(college)
    return colleges


def top_matches(preferences: List[Dict]) -> List[Dict]:
    """Returns the top matching colleges for a given set of preferences."""
    colleges = score_all_colleges(preferences)
    return sorted(colleges, key=lambda i: i["score"], reverse=True)[0:10]


def embed_description(description: str):
    if description == "":
        return ""
    else:
        embedding_df = pd.read_csv(
            "finalproject/collegesearch/college_data/embedding_dict.csv"
        )
        embedding = WordEmbedding(embedding_df)
        try:
            description_vector = embedding.embed_document(description).values
        except AttributeError:
            description_vector = ones(100)
        return description_vector


def calculate_match(preferences, college_info: List[Dict]) -> float:
    """This is the app's main feature, an algorithm that produces a match score
    based on preferences entered by the user and information about a college.
    Scores are generally in the range of 0-100 for realistic inputs, but you
    can land outside this interval by entering e.g. SAT scores not between
    200-800, or a desired student body size outside of 600-60,000.
    Our algorithm gives better scores to higher ranked schools and deducts
    points for high tuition cost and student body size dissimilar to
    the user's preference. MIT is the top university according to our
    scraped source data, so if their tuition were $0 and the user prefers
    a student population size of 4,350, it would receive a score of 100.

    The current algorithm is as follows:

    Score starts at +20.

    +/- 25 points * similarity between user input and a college's
    embedded wikipedia article vector. (If the user inputs no text,
    every college gets +25 points.)

    +/- 10 points * how closely the user's desired student population
    matches the college's population. (logarithmic scale)

    + 20 points - (college's Niche rank)/5. Top ranked MIT receives
    twenty points, #100 ranked UC Irvine receives none.

    +/- 10 points * [user's public/private preference matches school].
    If the user says no preference, every college gets +10 points.

    + 10 points if the college is in the user's preferred state; -1
    otherwise. +5 points if the college is in the user's preferred
    region, -2 otherwise. If state/region preferences are not entered,
    every college gets +10 and +5 points respectively.

    - 0.2 points * [college's tuition in thousands of dollars].
    A college loses one point for every $5,000 of their tuition rate.

    The above categories add up to 100 maximum, but with only 80 points
    possible for colleges at the bottom of the list. Two more adjustments
    are made based on the user's SAT scores:

    - 0.2 points * [college's 75th percentile SAT score - user's SAT score]
    - 0.2 points * [college's 25th percentile SAT score - user's SAT score]
    These deduct points from colleges where the user has a lower SAT score
    than the college's student body, so that the recommendations will show
    colleges matching the user's academic stats.

    + 0.1 points * [1600 - user's SAT score]
    This allows colleges lower on the list to receive scores nearly 100
    match points for applicants unlikely to attend the top schools.
    """
    score = 35

    # Describe the college you want to go to.
    if preferences["vector"] == "":
        score += 25
    else:
        similarity = cosine_similarity(
            preferences["vector"], college_info["description"]
        )
        score += 25 * similarity

    # How many undergraduates should the college have?
    x = preferences["size"]
    y = college_info["size"]
    size_match = 1 - (abs(log(x / y)))
    score += 10 * size_match

    # User's SAT scores
    sat = preferences["sat_verbal"] + preferences["sat_math"]
    if sat < college_info["sat_min"]:
        score += (sat - college_info["sat_min"]) / 5
    if sat < college_info["sat_max"]:
        score += (sat - college_info["sat_max"]) / 5
    score += (1600 - sat) / 10
    # 100 SAT points = 5 match points

    # College's ranking
    score += (100 - college_info[0]) / 5

    # Tuition
    price = int(re.sub("\D", "", college_info["price"]))
    score += -price / 5000

    # Do you prefer public colleges, private colleges, or neither?
    if preferences["public"] == 2:
        score += 10
    elif preferences["public"] == college_info["public"]:
        score += 10
    elif preferences["public"] != college_info["public"]:
        score += -10

    return round(score, 3)


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
        """Get cosine similarity for two matrices

        :returns: cosign similarity
        :rtype: int
        """
        # get dot product of the arrays
        numerator = np.dot(reference2, reference)
        # multiply vectors normalizatized
        dominator = np.linalg.norm(reference2) * np.linalg.norm(reference)
        return numerator / dominator

    def embed_document(self, text):
        """Convert text to vector, by finding vectors for each word and combining

        :param str text: the document (one or more words) to get a vector
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
        default = zeros(100)
        # getting a map of the dictionary vectors
        vec = map(lambda t: self.dict.get(t, default), tokenized)
        # reducing the matrixes via
        averaged_vec = reduce(lambda x, y: x + y, vec)
        return averaged_vec
