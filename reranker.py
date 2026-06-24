from sentence_transformers import (
    CrossEncoder
)

reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_documents(
    query,
    documents,
    top_k=12
):

    if not documents:

        return []

    pairs = [
        (
            query,
            doc.page_content
        )
        for doc in documents
    ]

    scores = (
        reranker_model.predict(
            pairs
        )
    )

    ranked_docs = sorted(
        zip(
            documents,
            scores
        ),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        doc
        for doc, _
        in ranked_docs[:top_k]
    ]