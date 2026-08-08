from AI.retrieval import Retriever
from AI.prompt import PromptBuilder
from AI.llm import GeminiLLM

class ChatService:
    """
    orchestrates(connduct or connect) the complete RAG pipeline.
    """
    def __init__(self):
        self.retriever=Retriever()
        self.llm = GeminiLLM()

    def chat(
            self,
            question: str,
            document_id: int
    ) -> dict:
        """Retrieves the chunks which is similar to the questions"""
        context_chunks = self.retriever.retrieve(
            question=question,
            document_id=document_id
        )

        """Build the correct prompt to return the result format"""
        prompt = PromptBuilder.build_chat_prompt(
            question=question,
            context_chunks=context_chunks
        )

        """Generate the answer for the question through llm(gemini)"""
        answer = self.llm.generate_response(
            prompt
        )

        """Return the Response to the user"""
        return{
            "question": question,

            "answer": answer,

            "context_chunks": context_chunks
        }
