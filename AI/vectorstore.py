import uuid
from qdrant_client.models import(
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

from database.qdrant import qdrant_client

class VectorStore:
    """it handles all the qdrant operations"""

    COLLECTION_NAME = "documents"
    VECTOR_SIZE=768

    @classmethod
    def create_collection(cls):
        """it is used for creating the collections"""
        collections = qdrant_client.get_collections()
        existing_collections = [
            collection.name
            for collection in collections.collections
        ]

        if cls.COLLETION_NAME not in existing_collections:
            qdrant_client.create_collection(
                collection_name = cls.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=cls.VECTOR_SIZE,
                    distance=Distance.COSINE
                )
            )
    """below store embedding function is used for storing the embeddings"""
    @classmethod
    def store_embeddings(
        cls,
        embeddings: list,
        chunks: list,
        document_id: int,
        original_filename: str
    ):
        points=[]

        for index, (embedding, chunk) in enumerate(
            zip(embeddings, chunks)
        ):
            point=PointStruct(

                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "document_id": document_id,
                    "chunk_index": index,
                    "chunk": chunk,
                    "filename": original_filename
                }
            )

            points.append(point)
        qdrant_client.upsert(
            collection_name=cls.COLLECTION_NAME,
            points=points
        )

    """this function is used for searching the similar chunks"""
    @classmethod
    def search(
        cls,
        query_embedding: list,
        top_k: int=5
    ):
        return qdrant_client.search(
            collection_name=cls.COLLECTION_NAME,
            query_vector=query_embedding,
            limit=top_k
        )

    """Search method to search within the document which is one single document"""
    @classmethod
    def search_document(
        cls,
        query_embedding: list,
        document_id: int,
        top_k: int=5
    ):
        return qdrant_client.search(
            collection_name=cls.COLLECTION_NAME,

            query_vector=query_embedding,

            limit=top_k,

            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(
                            value=document_id
                        )
                    )
                ]
            )
        )

    """Delete the unwanted documents from the Vectors"""
    @classmethod
    def delete_document(
        cls,
        document_id: int
    ):
        qdrant_client.delete(
            collection_name=cls.COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(
                            value=document_id
                        )
                    )
                ]
            )
        )