from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_llm():
    """
    Initialize LLM used across the project
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=OPENAI_API_KEY
    )

    return llm