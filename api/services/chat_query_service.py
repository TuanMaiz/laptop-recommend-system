from dotenv import load_dotenv
import os
import textwrap

# Langchain
from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain, GraphCypherQAChain
from langchain.prompts import PromptTemplate

import openai

# Load from environment
load_dotenv('.env', override=True)

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE') or 'neo4j'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize graph connection
kg = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    database=NEO4J_DATABASE,
)


# Cypher generation prompt
CYPHER_GENERATION_TEMPLATE = """Task: Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Note:
- Do not include explanations or apologies.
- Only output the Cypher statement.
- Ignore any questions that are not about constructing a Cypher statement.

Examples:
# What are the laptops that have 32GB RAM?
MATCH (laptops:Laptop)-[:HAS_COMPONENT]->(ram:RAM) 
WHERE ram.ramSizeGB = 32
RETURN laptops LIMIT 3;

The question is:
{question}"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"],
    template=CYPHER_GENERATION_TEMPLATE,
)
client = ChatOpenAI(
    temperature=0, 
    model="gpt-4o-mini", 
    base_url="https://routellm.abacus.ai/v1",
    api_key=OPENAI_API_KEY,
    
    )

def makeChat(message: Any):
    client = OpenAI(
        base_url="https://routellm.abacus.ai/v1",
        api_key=OPENAI_API_KEY,
    )

    stream = False  # or False
    chat_completion = client.chat.completions.create(
        model="route-llm",
        messages=[{"role": "user", "content": message}],
        stream=stream,
    )
    if stream:
        response_content = ""
        for event in chat_completion:
            if event.choices[0].finish_reason:
                break
            else:
                if event.choices[0].delta and event.choices[0].delta.content:
                    response_content += event.choices[0].delta.content
        return {"response": response_content}
    else:
        return {"response": chat_completion.choices[0].message.content}