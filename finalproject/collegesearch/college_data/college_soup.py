from bs4 import BeautifulSoup
import codecs
import pandas as pd
import numpy as np
import re
import wikipedia
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
            wiki = wikipedia.page(y.text).content
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
print(wiki_list)
