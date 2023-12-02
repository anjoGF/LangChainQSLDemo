---
# LangChain SQL Microservice README

## Introduction

In the evolving world of data engineering, the integration of natural language processing (NLP) with SQL databases has revolutionized data interactions. LangChain, a sophisticated library for building language model applications, enables querying SQL databases using natural language. This README will guide you through the process of setting up and using LangChain to develop a data engineering microservice, including setting up the Chinook database in a Jupyter Notebook environment. This setup closely follows LangChain documentation but adds additional steps to package the application and test it on an AWS EC2 instance in part 2 and 3.

## Prerequisites

Before getting started, make sure you have the following prerequisites:

- Basic knowledge of Python and SQL.
- An environment for running Jupyter Notebooks, such as Google Colab or JupyterLab.

## Step 1: Setting Up the Chinook Database

The Chinook database is an alternative to the Northwind database and represents a digital media store with various tables. Follow these steps to install the Chinook database in Google Colab:

1. **Download the Chinook Database SQL Script:**
   Use the `wget` command to download the Chinook database SQL script directly in your notebook:
   ```
   wget https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql
   ```

2. **Create and Populate the Database:**
   Run the script to create the Chinook database:
   ```
   sqlite3 Chinook.db < Chinook_Sqlite.sql
   ```

3. **Verify the Installation:**
   Execute a SQL query to confirm the database setup:
   ```
   sqlite3 Chinook.db "SELECT * FROM Artist LIMIT 10;"
   ```

## Step 2: Setting Up the Environment

Install the required packages by running the following command:
```
pip install langchain langchain-experimental openai
```

Configure your OpenAI API Key by setting it as an environment variable in your Jupyter Notebook:
```python
import os
os.environ['OPENAI_API_KEY'] = 'your_api_key_here'
```
Replace `'your_api_key_here'` with your actual OpenAI API key.

## Step 3: Creating the SQLDatabaseChain

LangChain allows the creation and execution of SQL queries based on natural language prompts. Create the SQLDatabaseChain as follows:

```python
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

# Connect to the Chinook database
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
llm = OpenAI(temperature=0, verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
```

## Step 4: Querying the Database

Query the database using a natural language prompt:

```python
import time

try:
    response = db_chain.run("How many employees are there?")
    print(response)
except Exception as e:
    if "RateLimitError" in str(e):
        print("Rate limit exceeded. Waiting before retrying...")
        time.sleep(60)
        response = db_chain.run("How many employees are there?")
        print(response)
    else:
        raise
```

## Step 5: Deep Dive into SQL Queries

LangChain's versatility allows for constructing and executing SQL queries from user questions:

```python
from langchain.chains import create_sql_query_chain
from langchain.chat_models import ChatOpenAI

chain = create_sql_query_chain(ChatOpenAI(temperature=0), db)
query = chain.invoke({"question": "How many employees are there"})
print(query)

print(db.run(query))
```

## Step 6: Enhancing the Microservice

Improve your microservice by customizing the database description, including dynamic examples, and implementing error recovery with SQL agents.

## Step 7: Implementing SQL Agents

SQL agents offer a flexible approach to database interaction:

```python
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType

agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0)),
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

print(agent_executor.run("Describe the playlisttrack table"))
```

## Testing in Jupyter Notebook

This guide includes a Jupyter Notebook with interactive code cells for experimenting with the microservice.

## Conclusion

Integrating LangChain with SQL databases for a data engineering microservice simplifies querying using natural language. This approach enhances data querying accessibility and fosters advanced applications in various fields.

Explore LangChain's capabilities in your Jupyter Notebook environment. Stay tuned for part 2 of 3.

Note: Always practice secure coding, especially when handling database connections and executing queries.

---
