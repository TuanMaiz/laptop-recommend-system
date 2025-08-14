from dotenv import load_dotenv
import os
import sys
from tqdm import tqdm

from langchain_neo4j import Neo4jGraph

try:
    # Load environment variables
    load_dotenv('.env', override=True)
    NEO4J_URI = os.getenv('NEO4J_URI')
    NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
    NEO4J_DATABASE = os.getenv('NEO4J_DATABASE')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # Validate required environment variables
    required_vars = {
        'NEO4J_URI': NEO4J_URI,
        'NEO4J_USERNAME': NEO4J_USERNAME,
        'NEO4J_PASSWORD': NEO4J_PASSWORD,
        'NEO4J_DATABASE': NEO4J_DATABASE
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    print("Environment variables loaded successfully")

except Exception as e:
    print(f"Error loading environment variables: {e}")
    sys.exit(1)

try:
    # Connect to the knowledge graph instance using LangChain
    print("Connecting to Neo4j database...")
    kg = Neo4jGraph(
        url=NEO4J_URI, 
        username=NEO4J_USERNAME, 
        password=NEO4J_PASSWORD, 
        database=NEO4J_DATABASE
    )
    print("Successfully connected to Neo4j database")

except Exception as e:
    print(f"Error connecting to Neo4j database: {e}")
    sys.exit(1)

def split_cypher_statements(cypher_content):
    """Split Cypher content into individual statements"""
    # Split by semicolon and filter out empty statements
    statements = [stmt.strip() for stmt in cypher_content.split(';') if stmt.strip()]
    return statements

try:
    # Read and execute Cypher query
    print("Reading Cypher query from file...")
    with open('cipher_outputs/neo4j_import.cypher', 'r') as file:
        cypher_content = file.read()
    
    if not cypher_content.strip():
        raise ValueError("Cypher query file is empty")
    
    # Split the content into individual statements
    statements = split_cypher_statements(cypher_content)
    print(f"Found {len(statements)} Cypher statements to execute")
    
    # Execute each statement individually with progress bar
    successful_executions = 0
    failed_executions = 0
    
    # Create progress bar with tqdm
    with tqdm(total=len(statements), desc="Executing Cypher statements", unit="stmt") as pbar:
        for i, statement in enumerate(statements, 1):
            try:
                # Update progress bar description with current statement number
                pbar.set_description(f"Executing statement {i}/{len(statements)}")
                
                result = kg.query(statement)
                successful_executions += 1
                
                # Update progress bar postfix with success count
                pbar.set_postfix({
                    'Success': successful_executions, 
                    'Failed': failed_executions
                })
                
                # Optionally print result for debugging (comment out for cleaner output)
                # if result:
                #     tqdm.write(f"Statement {i} result: {result}")
                    
            except Exception as stmt_error:
                failed_executions += 1
                # Use tqdm.write to print without interfering with progress bar
                tqdm.write(f"Error executing statement {i}: {stmt_error}")
                tqdm.write(f"Failed statement: {statement[:100]}...")  # Show first 100 chars
                
                # Update progress bar postfix with failure count
                pbar.set_postfix({
                    'Success': successful_executions, 
                    'Failed': failed_executions
                })
                
                # Continue with next statement instead of stopping
                continue
            finally:
                # Update progress bar
                pbar.update(1)
    
    print(f"\nExecution completed: {successful_executions} successful, {failed_executions} failed")
    
    if failed_executions > 0:
        print(f"Warning: {failed_executions} statements failed to execute")
    else:
        print("All Cypher statements executed successfully")

except FileNotFoundError:
    print("Error: Could not find 'cipher_outputs/neo4j_import.cypher' file")
    sys.exit(1)
except Exception as e:
    print(f"Error processing Cypher queries: {e}")
    sys.exit(1)

print("Neo4j population completed")