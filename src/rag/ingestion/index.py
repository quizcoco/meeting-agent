
def index_meeting(
    meeting_id,
    document,
    embedder, 
    vector_store
):

    embedding = embedder.embed(
        [document]
    )

    vector_store.add_documents(
        vectors=embedding,
        docs=[document],
        doc_ids=[meeting_id],
        metadatas=[
            {
                "meeting_id": meeting_id
            }
        ]
    )
