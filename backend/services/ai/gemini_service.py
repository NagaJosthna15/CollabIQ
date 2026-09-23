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
        last_error = None

        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                if not response or not response.text:
                    raise ValueError(
                        "Gemini returned an empty response"
                    )

                return response.text

            except Exception as e:
                last_error = e

                print(
                    f"Attempt {attempt + 1} failed: {type(e).__name__}"
                )

                if attempt < 2:
                    time.sleep(3)

        raise RuntimeError(
            "Gemini service is temporarily unavailable"
        ) from last_error