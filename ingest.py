from langchain_chroma import Chroma

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from document_loader import (
    load_repository_documents
)


EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

DB_PATH = "./chroma_db"


def create_vector_store(
    repo_path
):

    documents = (
        load_repository_documents(
            repo_path
        )
    )
    print(
        "Documents loaded:",
        len(documents)
        )
    if not documents:
        raise ValueError(
            "No documents were loaded from repository."
            )

    embeddings = (
        HuggingFaceEmbeddings(
            model_name=
            EMBEDDING_MODEL
        )
    )

    try:

        existing_db = Chroma(
            persist_directory=
            DB_PATH,

            embedding_function=
            embeddings
        )

        ids = existing_db.get().get(
            "ids",
            []
        )

        if ids:

            existing_db.delete(
                ids=ids
            )

    except:
        pass
    if not documents:
        raise ValueError(
            "No documents were loaded from repository."
            )

    vectordb = (
        Chroma.from_documents(
            documents=
            documents,

            embedding=
            embeddings,

            persist_directory=
            DB_PATH
        )
    )

    print(
        f"\nVector DB Ready"
    )

    print(
        f"Total Chunks Indexed: "
        f"{len(documents)}"
    )

    return (
        vectordb,
        documents
    )