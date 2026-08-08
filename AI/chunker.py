from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextChunker:
    """
    extracted text are divided into chunks
    """

    def __init__(
            self,
            chunk_size: int = 1000,
            chunk_overlap: int = 200,
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,

            Separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )
    def split_text(
            self,
            text: str
    ) -> list[str]:
        """
        this function is for splitting the stext into chunks
        """
        return self.text_splitter.split_text(text)