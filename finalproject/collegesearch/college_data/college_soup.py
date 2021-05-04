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
            if search == "Bowdoin College":
                search = 'bowden college'
            if search == "Williams College":
                search = 'william college'
            if search == 'Northeastern University':
                search = 'north western university'
            if search == 'Kenyon College':
                search = 'kenyan college'
            if search == 'William & Mary':
                search = 'College of William & Mary'
            wiki = wikipedia.page(search).content
            wiki_list.append(wiki)
        for z in x.select(".search-result-fact"):
            for q in z.select(".search-result-fact__label"):
                for w in z.select(".search-result-fact__value"):
                    if q.text == "Acceptance Rate":
                        feature = attend
                        feature.append(w.text)
                    if q.text == "Net Price":
                        feature = price
                        feature.append(w.text)
                    if q.text == "SAT Range":
                        feature = sat
                        feature.append(w.text)
tokenized_sentences = np.array(list(map(WordEmbedding.tokenize,wiki_list)))
model = Word2Vec(tokenized_sentences, window=2, min_count=0, vector_size=100, workers=4)
words = model.wv.key_to_index
we_dict = {word:reduce(lambda x, y: x + y,model.wv[word]) for word in words}
embedding = WordEmbedding(we_dict)
embeddings = np.array(list(map(embedding.embed_document,wiki_list)))
college_embedding = pd.DataFrame(embeddings,names)
college_facts = {'embeddings':embeddings, 'sat': sat, 'names': names, 'price': price, 'attend': attend}
college_embedding.to_csv('embedding.csv')
