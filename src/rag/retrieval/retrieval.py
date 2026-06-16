from src.repository.rds_repository import get_meeting


class Retriever:

    def __init__(
        self,
        embedder,
        vector_store
    ):
        self.embedder = embedder
        self.vector_store = vector_store


    def retrieve(
        self,
        query,
        k=10
    ):  
      
        query_vector = self.embedder.embed(
        [query]
    )
        results = self.vector_store.search_vector(
        query_vector,
        k
    )

        meetings = []

        for hit in results:

            meeting = get_meeting(
                hit["id"]
            )

            meetings.append(meeting)

        return meetings