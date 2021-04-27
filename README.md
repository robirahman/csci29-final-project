# csci29-final-project
Advanced Python for Data Science final project

CSCI E-29 project proposal, Cary Judson and Robi Rahman

We want to make a web app that helps high schoolers decide where to apply to college. It would run on Django, with a frontend webpage that takes input from the user about their preferences (such as small vs large universities, geographical region, etc), queries a database with information about e.g. 100 colleges, computes some scoring functions that assess how well each college fits the user's preferences, and produces recommendations.

Example: user wants to go to university in the northeast, at a private school that has around 7000 undergraduates, and they have an SAT score of 1500 -> app recommends they should apply to Harvard.

Similarly to Pset 3's document embeddings, we can compute comparisons between different universities, so that users could also type in a specific college they are interested in and the app will show similar ones from the database. During the course of this project we will learn how to query stored data using the Django framework, and use python to perform computations using this data as input and then deliver results to the user.

Cary:

1. Implement workflow via luigi

2. NLP of essay responses (for toy data we will use learn.parquet from pset3 and the first paragraph of colleges wikipedia articles)

Robi:

1. Models (python classes that structure the database).

2. Django web frontend

Shared:

1. calculations that score colleges based on the user input on forced choice questions.