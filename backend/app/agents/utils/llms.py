import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


class LLMModel:
    @staticmethod
    def get_model(model_name: str = None):
        model = model_name or os.getenv("OPENAI_MODEL")
        base_url = os.getenv("OPENAI_BASE_URL")
        api_key = os.getenv("OPENAI_API_KEY")

        if not model:
            raise ValueError("OPENAI_MODEL is missing in .env and no model_name provided")
        if not base_url:
            raise ValueError("OPENAI_BASE_URL is missing in .env")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing in .env")

        return ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=0
        )
