import pandas as pd
from bs4 import BeautifulSoup
import codecs
import wikipedia
from gensim.models import Word2Vec
import requests
from prefect import task, Flow
import numpy as np
from embedding import WordEmbedding
from prefect.agent.local import LocalAgent

def college_facts():
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
                if name == 'William & Mary':
                    name = 'College of William & Mary'
                search = wikipedia.search(y.text)[0]
                gov_api = requests.get(
                    "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.name=" + name + "&fields=id,school.name,school.state,2018.student.size&api_key=Cs0K2iI7mMCdblkudyJjzzkhntdNgRzyUgrSHFPk").json()
                if search == "Northwestern University":
                    search = "north western university"
                elif search == "Bowdoin College":
                    search = 'bowden college'
                elif search == "Williams College":
                    search = 'william college'
                elif search == 'Northeastern University':
                    search = 'north western university'
                elif search == 'Kenyon College':
                    search = 'kenyan college'
                wiki = wikipedia.page(search).content
                wiki_list.append(wiki)
                if name == 'William & Mary':
                    size.append(6300)
                    state.append('VA')
                if name == 'Massachusetts Institute of Technology':
                    size.append(4500)
                    state.append('MA')
                elif name == 'Washington University in St. Louis':
                    size.append(7356)
                    state.append('WA')
                elif name == 'Colby College':
                    size.append(2000)
                    state.append('ME')
                elif name == 'Washington & Lee University':
                    size.append(1822)
                    state.append('VA')
                elif name == 'The Cooper Union for the Advancement of Science and Art':
                    size.append(845)
                    state.append('NY')
                elif name == 'Texas A&M University':
                    size.append(60000)
                    state.append('TX')
                elif name == 'The Ohio State University':
                    size.append(50000)
                    state.append('OH')
                else:
                    size.append(gov_api['results'][0]['2018.student.size'])
                    state.append(gov_api['results'][0]['school.state'])
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
            data = {'wiki_list': wiki_list, 'sat': sat, 'names': names, 'price': price, 'acceptance': attend,
                    'size': size, 'state': state}
    college_facts = pd.DataFrame(data=data)
    college_facts.to_csv('facts.csv')

@task(log_stdout=True,nout=2)
def college_embeddings(list):
    wiki_list = list['wiki_list']
    names = list['names']
    tokenized_sentences = np.array(list(map(WordEmbedding.tokenize,wiki_list)))
    model = Word2Vec(tokenized_sentences, window=2, min_count=0, vector_size=100, workers=4)
    words = model.wv.key_to_index
    we_dict = {word:model.wv[word] for word in words}
    embedding = WordEmbedding(we_dict)
    embeddings = np.array(list(map(embedding.embed_document,wiki_list)))
    college_embedding = pd.DataFrame(embeddings,names)
    college_embedding.to_csv('embedding.csv')
    return college_embedding

with Flow("data analysis") as flow:
    college_facts = college_facts()
    college_embedding = college_embeddings(college_facts)
 
flow.register(project_name="college")
LocalAgent().start()
flow.run()
