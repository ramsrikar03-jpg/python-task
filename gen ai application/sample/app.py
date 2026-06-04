import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
except ImportError:
    genai = None


def generate(question: str):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set. Update .env or your environment variables.")
        return

    if genai is None:
        print("Error: google-genai is not installed.")
        print("Install it with: python -m pip install -r requirements.txt")
        return

    client = genai.Client(api_key=api_key)
    model = "gemini-3-flash-preview"

    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=question,
        ):
            if text := chunk.text:
                print(text, end="")
    except Exception as exc:
        print("Request failed:", exc)


if __name__ == "__main__":
    question = input("Enter your question: ")
    generate(question)