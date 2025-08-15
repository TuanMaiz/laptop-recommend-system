# main.py
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from neo4j import GraphDatabase
from models import Base, Laptop, LaptopImage, LaptopSpecification
from importers import import_to_sql

# Load data
with open('sazo_laptops.json', 'r', encoding='utf-8') as f:
    laptops_data = json.load(f)

# Setup SQL database
engine = create_engine('sqlite:///laptops.db')  # or your preferred DB
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Import to SQL
import_to_sql(session, laptops_data)

# Neo4j import (keep your existing script)
# You can call your create_laptop_cypher function here
cypher_output = create_laptop_cypher(laptops_data)

# Write to file or execute directly with Neo4j driver
with open("neo4j_import.cypher", "w", encoding="utf-8") as f:
    f.write(cypher_output)
    print(f"Cypher queries written to neo4j_import.cypher")

# Optional: Execute directly with Neo4j driver
# with GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password")) as driver:
#     with driver.session() as neo4j_session:
#         neo4j_session.run(cypher_output)