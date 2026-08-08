class PromptBuilder:
    """
    Builds prompts for the Gemini model.
    """
    @staticmethod
    def build_chat_prompt(
        question: str,
        context_chunks: list[str]
    ) -> str:
        """
        Build a prompt for document question answering.
        """

        context = "\n\n".join(context_chunks)

        prompt = f"""
You are an Enterprise Document Intelligence Assistant.

Your job is to answer ONLY from the uploaded document.

Instructions:
1.Read the provided document context carefully.

2.Answer only from context.

3.If the answer is not available, reply:
  "I couldn't find the answer in the uploaded document."

4.Do not make up information.

5.Keep the answer clear and professional.

==========================
extract the content from the document
==========================

{context}

==========================
gets the question from the user
==========================
{question}

==========================
generat answer for user question
==========================
"""
        
        return prompt
