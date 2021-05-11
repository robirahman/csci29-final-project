# csci29-final-project

## Advanced Python for Data Science final project
by Cary Judson and Robi Rahman

### Project Proposal

We want to make a web app that helps high schoolers decide where to apply to college. It would run on Django, with a
frontend webpage that takes input from the user about their preferences (such as small vs large universities,
geographical region, etc), queries a database with information about e.g. 100 colleges, computes some scoring functions
that assess how well each college fits the user's preferences, and produces recommendations.

Example: user wants to go to university in the northeast, at a private school that has around 7000 undergraduates, and
they have an SAT score of 1500 -> app recommends they should apply to Harvard.

Similarly to Pset 3's document embeddings, we can compute comparisons between different universities, so that users
could also type in a specific college they are interested in, and the app will show similar ones from the database.
During the course of this project we will learn how to query stored data using the Django framework, and use python to
perform computations using this data as input and then deliver results to the user.

### Project Scope

Cary:

1. Implement web scraping and data loading workflow via Prefect.
2. NLP of Wikipedia articles to train word2vec model and embed college descriptions.
3. GitHub Actions to deploy Sphinx documentation pages.

Robi:

1. ORM models to set up SQLite database of college information.
2. Django web server and frontend HTML forms.
3. Calculations that score colleges based on the user's input.

### Project Initialization Workflow

The project begins with Niche's top 100 list of [Best colleges in America](https://www.niche.com/colleges/search/best-colleges/),
scraped from their website and then saved to an S3 bucket. We decided to use Niche rather than the more popular rankings
such as US News because they publish a combined list that includes research universities and liberal arts colleges,
whereas US News ranks them separately in such a way that you cannot determine relative placement between colleges on different
lists. The scraped HTML from Niche is then processed using Beautiful Soup, where relevant facts are collected by analyzing the HTML.
For facts not available from the Niche list, such as student body population, in-state and out-of-state tuition, the workflow
then queries the US Department of Education's [College Scorecard API](https://collegescorecard.ed.gov/data/documentation/).
To obtain descriptions of each college, the workflow fetches the contents of their Wikipedia entries using the
[Wikipedia python library](https://pypi.org/project/wikipedia/). These pages are then tokenized and provided to word2vec
to train a word embedding model similar to the one used for Pset 3; the wikipedia articles are then embedded and stored
as a numeric vector representing the description of each college. The vectors and college data are then saved into a
SQLite database which will be used by the web app.
This workflow is executed by Prefect, a task automation and scheduling package which is similar to Luigi but more readable and
user-friendly. The workflow is organized into tasks and flows, designated by simply placing a Prefect `@task` decorator on each step.


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


### Application Deployment

Once the workflow has completed, the app is ready for deployment. Upon running the Django server, the app hosts a web
form with a survey of different aspects of colleges, including a free response text field. The user can fill in their
preferences and a description of their desired college, and then submit the form. This triggers a POST request, from
which Django obtains their inputs, and computes a match score based on the similarity of the user's responses to the
data about each college, queried from the database which was populated by the workflow. The server then returns the top
10 colleges by match score and displays them on a results page.

The database models are designed using a snowflake schema with college locations stored as foreign keys to states rather
than as strings. This allows states to be grouped into regions, and users can specify a preference to attend college in
a geographical region, in which case colleges in those states are elevated in the results. See the docstrings for the
Django models for details.

### Project Conclusions

In conclusion, it can be said this project demonstrates how to wrangle data. It is noteworthy that Niche charges money
for their api, most of which can be obtained via html files and python. This project also possibly makes a better college
matching app then any other on the internet. We have a free response form, and our results are quantitative rather than
categorical. This project also can teach someone how to work with Prefect, Beautiful Soup, and the Wikipedia pypi package.
The code was made more readable then advanced, to enable coders to learn.

