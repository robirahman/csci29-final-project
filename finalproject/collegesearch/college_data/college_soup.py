import re
import pandas as pd
from bs4 import BeautifulSoup
import codecs
import wikipedia
from gensim.models import Word2Vec
from functools import reduce
import numpy as np
from embedding import WordEmbedding
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
tokenized_sentences = np.array(list(map(WordEmbedding.tokenize,wiki_list)))
model = Word2Vec(tokenized_sentences, window=2, min_count=0)
words = model.wv.key_to_index
we_dict = {word:reduce(lambda x, y: x + y,model.wv[word]) for word in words}
embedding = WordEmbedding(we_dict)
embeddings = np.array(list(map(embedding.embed_document,wiki_list)))
college_embedding = pd.DataFrame(embeddings,names)
