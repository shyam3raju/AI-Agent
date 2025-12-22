import os
import requests
from sqlalchemy import create_engine
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent

os.environ["GOOGLE_API_KEY"] = "Gemini api key"
os.environ["LANGSMITH_API_KEY"] = "Langsmith api key"
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "chinook-sql-agent"

DB_FILE = "chinook.db"
CHINOOK_URL = (
    "https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
)

if not os.path.exists(DB_FILE):
    print("⬇️ Downloading Chinook database...")
    response = requests.get(CHINOOK_URL)
    response.raise_for_status()
    with open(DB_FILE, "wb") as f:
        f.write(response.content)
    print("✅ Chinook database downloaded")
else:
    print("✅ Chinook database already exists")


engine = create_engine(f"sqlite:///{DB_FILE}")
db = SQLDatabase(engine)

print("📊 Tables:", db.get_usable_table_names())


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


toolkit = SQLDatabaseToolkit(
    db=db,
    llm=llm
)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

questions = [
    "Which customer spent the most money?",
    "List the top 5 artists by number of albums",
    "What is the total revenue by country?",
    "List the top 10 tracks by total sales"
]

for q in questions:
    print(f"Question: {q}")
    result = agent.run(q)
    print(f"Answer:\n{result}")