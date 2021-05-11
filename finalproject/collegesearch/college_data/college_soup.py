
from prefect import task, Flow, Parameter
from embedding import college_embeddings, college_facts, create_wiki, create_dict
from prefect.engine.results import LocalResult
from prefect.engine.serializers import PandasSerializer
with Flow("data analysis") as flow:
    """take all the python functions and feed them into prefect
    
        :returns: n/a
        :rtype: n/a
    """
    bypass = Parameter("bypass", default=False, required=False)


    @task(log_stdout=True, nout=4,
          result=LocalResult(serializer=PandasSerializer(file_type='csv'), dir='/', location="facts.csv"))
    college_fact = college_facts(bypass=bypass)
    @task(log_stdout=True, nout=4,
          result=LocalResult(serializer=PandasSerializer(file_type='csv'), dir='/', location="wiki_list.csv"))
    wiki_list = create_wiki(college_fact, bypass=bypass)
    @task(log_stdout=True, nout=4,
          result=LocalResult(serializer=PandasSerializer(file_type='csv'), dir='/', location="embedding_dict.csv"))
    dict = create_dict(wiki_list, bypass=bypass)
    @task(log_stdout=True, nout=4,
          result=LocalResult(serializer=PandasSerializer(file_type='csv'), dir='/', location="college_embeddings.csv"))
    college_embedding = college_embeddings(dict, wiki_list, college_fact, bypass=bypass)
#run functions
flow.register(project_name="college")
# LocalAgent().start()
flow.run(bypass=False)
