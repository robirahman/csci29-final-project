from bs4 import BeautifulSoup
import codecs
import pandas as pd
import numpy as np
import re
html = codecs.open("niche_college_list_1.html")
soup = BeautifulSoup(html, 'html.parser')

names = []
attend = []
price = []
sat = []
for x in soup.select(".card__inner"):
    for y in x.select(".search-result__title"):
        names.append(y.text)
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
df = pd.DataFrame(np.array([[names], [attend], [price], [sat]]),

                   columns=['Name', 'Acceptance Rate', 'Net Price', 'SAT Range'])

