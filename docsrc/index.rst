.. College Search E-29 documentation master file, created by
   sphinx-quickstart on Tue May 11 18:36:10 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to College Search E-29's documentation!
===============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

csci29-final-project
====================



Advanced Python for Data Science final project
----------------------------------------------

by Cary Judson and Robi Rahman

Project Proposal
~~~~~~~~~~~~~~~~

We want to make a web app that helps high schoolers decide where to
apply to college. It would run on Django, with a frontend webpage that
takes input from the user about their preferences (such as small vs
large universities, geographical region, etc), queries a database with
information about e.g. 100 colleges, computes some scoring functions
that assess how well each college fits the user’s preferences, and
produces recommendations.

Example: user wants to go to university in the northeast, at a private
school that has around 7000 undergraduates, and they have an SAT score
of 1500 -> app recommends they should apply to Harvard.

Similarly to Pset 3’s document embeddings, we can compute comparisons
between different universities, so that users could also type in a
specific college they are interested in, and the app will show similar
ones from the database. During the course of this project we will learn
how to query stored data using the Django framework, and use python to
perform computations using this data as input and then deliver results
to the user.

Project Scope
~~~~~~~~~~~~~

Cary:

1. Implement web scraping and data loading workflow via Prefect.
2. NLP of Wikipedia articles to train word2vec model and embed college
   descriptions.
3. GitHub Actions to deploy Sphinx documentation pages.

Robi:

1. ORM models to set up SQLite database of college information.
2. Django web server and frontend HTML forms.
3. Calculations that score colleges based on the user’s input.

Project Initialization Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The project begins with Niche’s top 100 list of `Best colleges in
America <https://www.niche.com/colleges/search/best-colleges/>`__,
scraped from their website and then saved to an S3 bucket. We decided to
use Niche rather than the more popular rankings such as US News because
they publish a combined list that includes research universities and
liberal arts colleges, whereas US News ranks them separately in such a
way that you cannot determine relative placement between colleges on
different lists. The scraped HTML from Niche is then processed using
Beautiful Soup, where relevant facts are collected by analyzing the
HTML. For facts not available from the Niche list, such as student body
population, in-state and out-of-state tuition, the workflow then queries
the US Department of Education’s `College Scorecard
API <https://collegescorecard.ed.gov/data/documentation/>`__. To obtain
descriptions of each college, the workflow fetches the contents of their
Wikipedia entries using the `Wikipedia python
library <https://pypi.org/project/wikipedia/>`__. These pages are then
tokenized and provided to word2vec to train a word embedding model
similar to the one used for Pset 3; the wikipedia articles are then
embedded and stored as a numeric vector representing the description of
each college. The vectors and college data are then saved into a SQLite
database which will be used by the web app. This workflow is executed by
Prefect, a task automation and scheduling package which is similar to
Luigi but more readable and user-friendly. The workflow is organized
into tasks and flows, designated by simply placing a Prefect ``@task``
decorator on each step.

::

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

Application Deployment
~~~~~~~~~~~~~~~~~~~~~~

Once the workflow has completed, the app is ready for deployment. Upon
running the Django server, the app hosts a web form with a survey of
different aspects of colleges, including a free response text field. The
user can fill in their preferences and a description of their desired
college, and then submit the form. This triggers a POST request, from
which Django obtains their inputs, and computes a match score based on
the similarity of the user’s responses to the data about each college,
queried from the database which was populated by the workflow. The
server then returns the top 10 colleges by match score and displays them
on a results page.

The database models are designed using a snowflake schema with college
locations stored as foreign keys to states rather than as strings. This
allows states to be grouped into regions, and users can specify a
preference to attend college in a geographical region, in which case
colleges in those states are elevated in the results. See the docstrings
for the Django models for details.

Project Conclusions
~~~~~~~~~~~~~~~~~~~

During this project, we gained experience with various aspects of Python
programming. Web scraping was a new challenge not explored earlier in
the class, but we were able to find and apply several packages that made
it easy to collect valuable data. It is noteworthy that Niche sells the
data we needed through a premium subscription service, but as advanced
python programmers, it is possible to obtain it for free using open
source tools, and even automate the process.

Advanced python concepts were applied in several ways to optimize the
project’s implementation. The Prefect library’s ``@task`` decorator can
be applied to any functions to wrap them into the workflow. Partial
function evaluation was helpful when processing a set of user inputs, by
binding it to the general function that computes the match between any
student and any college, and returning a specific function that computes
the match between any college and a *specific* student. This function
can then be applied in a functional, vectorized manner to each college
in the dataset, to efficiently find the top matches. Predicate pushdown
on matching state or region foreign keys reduces computational overhead
while finding colleges that match a student’s location preferences.

The final product, our college recommendation engine, produces better
recommendations than any of the major alternatives available online from
large companies such as College Board, US News, and Niche. Most of them
are categorical, and work by ruling out schools that are not exact
matches for a student’s query: for example, they ask if you want to join
a fraternity in college, and if you say yes (/no) they only show
colleges that do (/don’t) have fraternities. Our app is quantitative and
still might put a college in your top 10 if it is different from one
desired aspect but fulfills most of your other preferences. We also have
a free response form that processes descriptions; there are similar
alternatives, such as CollegeBoard’s BigFuture, but those search for
matching keywords rather than judging similarity of meaning or
qualities.
