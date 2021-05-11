# csci29-final-project
Advanced Python for Data Science final project

CSCI E-29 project proposal, Cary Judson and Robi Rahman

We want to make a web app that helps high schoolers decide where to apply to college. It would run on Django, with a frontend webpage that takes input from the user about their preferences (such as small vs large universities, geographical region, etc), queries a database with information about e.g. 100 colleges, computes some scoring functions that assess how well each college fits the user's preferences, and produces recommendations.

Example: user wants to go to university in the northeast, at a private school that has around 7000 undergraduates, and they have an SAT score of 1500 -> app recommends they should apply to Harvard.

Similarly to Pset 3's document embeddings, we can compute comparisons between different universities, so that users could also type in a specific college they are interested in and the app will show similar ones from the database. During the course of this project we will learn how to query stored data using the Django framework, and use python to perform computations using this data as input and then deliver results to the user.

The start of the cycle of the data begins with a html file of niche we uploaded to s3. That html file is then feed into beautiful soup, where relevant facts are collected by analyzing the html. Some data points are also grabbed from collegescoreboard api. The package wikipedia is used to grab a list of wikipedia page contents saved as strings. These pages are all tokenized and feed into word2vec to create a vector/word model to then embed the wikipedia articles to make a college embeddings that are compared to a user's free response field and similarity is calculated using the wordembedding class we made in pset 3. The college facts are also fed into the user's recommendations. This workflow is wrapped in prefect, a tool like luigi but uses normal python functions and classes that are simply wrapped in a decorator. This has many advantages, as it allows for easier to read code and is much more user friendly. 


    @task(log_stdout=True,nout=4,result=LocalResult(serializer=PandasSerializer(file_type='csv'),dir='./',location="facts.csv"))

    for x in soup.select(".card"):
        if x.find(string="Sponsored") is None:
            for y in x.select(".search-result__title"):
                name = y.text
                names.append(name)
                
    size.append(gov_api["results"][0]["2018.student.size"])
    state.append(gov_api["results"][0]["school.state"])

    wiki_list = []
    for search in names:
        #search wikipedia
        wiki = wikipedia.page(search).content
        #save wikipedia page text in list
        wiki_list.append(wiki)
    data = {'wiki': wiki_list}
    wiki_list = pd.DataFrame(data=data)
    return wiki_list

    wiki_list = wiki_list['wiki'].to_list()
    tokenized_sentences = np.array(list(map(WordEmbedding.tokenize, wiki_list)))
    model = Word2Vec(tokenized_sentences, window=2, min_count=0, vector_size=100, workers=4)
    words = model.wv.key_to_index
    we_dict = {word: model.wv[word] for word in words}
    #basically, feed it into pset 3 stuff, no explain needed
    embedding = WordEmbedding(we_dict)
    embeddings = np.array(list(map(embedding.embed_document, wiki_list)))

    embedding = WordEmbedding(we_dict)
    embeddings = np.array(list(map(embedding.embed_document, wiki_list)))
    college_embedding = pd.DataFrame(embeddings, names)

Cary:

1. Implement workflow via prefect.

2. NLP of essay responses.

Robi:

1. Models (python classes that structure the database).

2. Django web frontend

Shared:

1. calculations that score colleges based on the user input on forced choice questions.
