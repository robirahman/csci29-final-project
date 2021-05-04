from bs4 import BeautifulSoup
import codecs
import wikipedia
from gensim.models import Word2Vec
import re
import numpy as np
html = codecs.open("niche_college_list_1.html")
soup = BeautifulSoup(html, 'html.parser')

names = []
attend = []
price = []
sat = []
wiki_list = []
for x in soup.select(".card"):
    if x.find(string="Sponsored") is None:
        for y in x.select(".search-result__title"):
            names.append(y.text)
            search = wikipedia.search(y.text)[0]
            if search == "Northwestern University":
                search = "north western university"
            wiki = wikipedia.page(search).content
            wiki_list.append(wiki)
        for z in x.select(".search-result-fact"):
            for q in z.select(".search-result-fact__label"):
                if q.text == "Acceptance Rate":
                    feature = attend
                if q.text == "Net Price":
                    feature = price
                if q.text == "SAT Range":
                    feature = sat
                    for w in z.select(".search-result-fact__value"):
                        feature.append(w.text)
def tokenize(text):
    """Get all "words", including contractions
    Example::
        tokenize("Hello, I'm Scott") --> ['hello', "i'm", 'scott']
    :returns: list of words in statement.
    :rtype: list
    """
    return re.findall(r"\w[\w']+", text.lower())
tokenized_sentences = np.array(list(map(tokenize,wiki_list)))
model = Word2Vec(tokenized_sentences, window=2, min_count=0)
words = model.wv.key_to_index()
we_dict = {word:model.wv[word] for word in words}
