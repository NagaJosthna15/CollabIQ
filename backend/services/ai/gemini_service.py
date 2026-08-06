import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiService:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash"
        )


    def generate(
        self,
        prompt
    ):

        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                return response.text

            except Exception as e:

                print(
                    f"Attempt {attempt+1} failed..."
                )

                time.sleep(3)

        raise Exception(
            "Gemini API unavailable after retries."
        )