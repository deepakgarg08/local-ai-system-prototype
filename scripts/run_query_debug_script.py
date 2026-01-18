from pipelines.query.run_rag import run_rag

if __name__ == "__main__":
    # query = "What does the system say about contract termination periods?"
    query = "Who won the FIFA world cup in 2014??"

    answer = run_rag(query, top_k=4)

    print("\n--- ANSWER ---\n")
    print(answer)
