from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    """
        the chunks are converted into embeddings
        """

    def __init__(
            self, 
            model_name: str = "BAAI/bge-base-en-v1.5"
    ):
        self.model = SentenceTransformer(model_name)
    def generate_embedding(
            self,
            text: str
    ) -> list[float]:
        """
        the embedding was done was single text which means one particular character contains
        one particular number individually
        """
        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )
        return embedding.tolist()

    def generate_embeddings(
            self, 
            texts: list[str]
    ) -> list[list[float]]:
        """
        the embeddings was done was all the chunks
        """
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()