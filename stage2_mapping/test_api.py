import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("\n Error: OPENAI_API_KEY is missing in .env!")
else:
    print(f"Loaded API Key: {api_key[:7]}...{api_key[-4:]}")
    try:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)
        response = llm.invoke("Hello, reply with 'API Working!' if you receive this.")
        print("\n Success! OpenAI API Response:")
        print(response.content)
    except Exception as e:
        print("\n Error connecting to API:")
        print(e)