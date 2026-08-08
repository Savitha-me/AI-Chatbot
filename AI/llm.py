import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiLLM:
    """
    communicates with the gemini model.
    """
    def __init__(self):
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError(
                "API KEY not found or invalid"
            )
        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )
    def generate_response(
            self,
            prompt: str
    ) -> str:
        """
        send the prompt to the gemini model and that model sends the respose to the user
        """
        try:
            response = self.model.generate_content(
                prompt
            )
            return response.text
        except Exception as e:
            raise Exception(
                f"Gemini Error: {str(e)}"
            )