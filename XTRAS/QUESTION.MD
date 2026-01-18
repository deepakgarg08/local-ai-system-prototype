I HAVE TWO QUESITON, INSPITE OF FIRST PUTTING THE QUERY INTO EMBEDDING DIRECTLY, I also learned a new approach, where query also first goes to the llm, which structure the query first in very well manner and then it is embeded and then goes to vector database. explain me the implemented approach and this approach, is this approach exist, if yes in what cases they are used?

caching, roles

indexing vs caching?
next time logging should be implemented
try catch/sanity check whether folder exists or not and also for filess

deployment, mlflow

logging

What is NOT implemented yet (important distinction)

Just to avoid confusion:

Feature	Implemented?
FAISS retrieval	✅ DONE
Prompt assembly	❌ NOT YET
LLM inference	❌ NOT YET
Reranking / MMR	❌ NOT YET
Hybrid BM25+FAISS ❌ NOT YET

how many steps are remaining for the prototyping part. not asking for main data implementation
do remember we have to deploy it also 

context engineering

need to add separate file where any type of online llm can be connected via api, option of connecting must be there 

NEED TO ADD MULTIPLE LLMS CONFIG, LIKE CLAUDE, GEMINI, MISTRAL, QWEN (ONLINE)
