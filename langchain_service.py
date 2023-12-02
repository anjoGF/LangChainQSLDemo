
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

class LangChainService:
    def __init__(self, db_path, openai_api_key):
        self.db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        self.llm = OpenAI(openai_api_key=openai_api_key, temperature=0)
        self.db_chain = SQLDatabaseChain.from_llm(self.llm, self.db, verbose=True)

    def query_database(self, query):
        try:
            return self.db_chain.run(query)
        except Exception as e:
            return str(e)
