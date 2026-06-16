from src.repository.rds_repository import get_recent_minutes

def get_recent_meetings(limit=3):

    return get_recent_minutes(limit)


def search_meetings(query, retriever):

    return retriever.retrieve(query)