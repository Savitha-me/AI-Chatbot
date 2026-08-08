from AI.embedding import EmbeddingGenerator
from AI.vectorstore import VectorStore

class Retriever:
    """
    gets the user input search in the vector db and get the most relevant results and show to user
    """
    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()

    def retrieve(
            self,
            question: str,
            document_id: int,
            top_k: int=5
    ) -> list[str]:
        """
        the whole function is used to find and get the relevant one
        """

        """
        the user input was converted as embedding and store in vector db
        """
        query_embedding = self.embedding_generator.generate_embedding(
            question
        )

        """
        using the search method search the relevant information
        """
        results = VectorStore.search_document(
            query_embedding=query_embedding,

            document_id=document_id,

            top_k=top_k
        )

        """
        the similar items found through search method was extracted to move to prompt field
        """
        chunks=[]
        for result in results:
            chunks.append(
                result.payload["chunk"]
            )
        return chunks