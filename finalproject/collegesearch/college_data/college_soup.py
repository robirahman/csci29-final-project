import re
import pandas as pd
from bs4 import BeautifulSoup
import codecs
import wikipedia
from luigi.local_target import LocalTarget
from luigi import ExternalTask, Parameter, Task
from gensim.models import Word2Vec
import requests
from functools import reduce
import numpy as np
from embedding import WordEmbedding
import luigi
class LocalFile(Task):  ##pargma: no cover
    """
    Gives the local html to use as a target
    """

    def output(self):
        return LocalTarget(
            "./niche_college_list_1.html", format=luigi.format.Nop
        )
class Embeddings(Task):
    """embeds the wikipedia articles with Word2Vec and wikipedia api via luigi
    input: list of colleges
    output: csv containing the embedding vectors and words"""
    def output(self):
        return LocalTarget(
            "./embedding.csv", format=luigi.format.Nop
        )
    def run(self):
        html = codecs.open("niche_college_list_1.html")
        soup = BeautifulSoup(html, 'html.parser')
        names = []
        attend = []
        price = []
        sat = []
        wiki_list = []
        state = []
        size = []
        for x in soup.select(".card"):
            if x.find(string="Sponsored") is None:
                for y in x.select(".search-result__title"):
                    name = y.text
                    names.append(name)
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

                    gov_api = requests.get(
                        "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.name=" + name + "&fields=id,school.name,school.state,2018.student.size&api_key=Cs0K2iI7mMCdblkudyJjzzkhntdNgRzyUgrSHFPk").json()
                    size.append(gov_api['results'][0]['2018.student.size'])
                    state.append(gov_api['results'][0]['school.state'])
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
        tokenized_sentences = np.array(list(map(WordEmbedding.tokenize, wiki_list)))
        model = Word2Vec(tokenized_sentences, window=2, min_count=0, vector_size=100, workers=4)
        words = model.wv.key_to_index
        we_dict = {word: model.wv[word] for word in words}
        embedding = WordEmbedding(we_dict)
        embeddings = np.array(list(map(embedding.embed_document, wiki_list)))
        college_facts = {'embeddings': embeddings, 'sat': sat, 'names': names, 'price': price, 'acceptance': attend,
                         'size': size, 'state': state}
        college_embedding = pd.DataFrame(data=college_facts)
        college_embedding.to_csv('embedding.csv')
class Facts(Task):
    """grabs relevent facts from html pages from niche using BeutifulSoup via luigi
    input: html from niche
    output: csv containing college facts"""
