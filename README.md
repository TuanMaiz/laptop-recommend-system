## Project Plan

This project implements a web scraping and data processing pipeline for laptop data from Sazo website, with both graph database (Neo4j) and relational database (SQL) storage options.

## Steps

1. **Run scraper to get scraped data** - done

   - Execute the web scraper to collect laptop data from Sazo website
   - Output: `sazo_laptop.json` file containing structured laptop information

2. **Generate Neo4j Cypher queries** - done

   - Run `scraped_data_to_cipher_neo4j` to convert scraped data into Cypher queries
   - Purpose: Import data into Neo4j graph database for relationship analysis

3. **Import data into SQL database** - ongoing

   - Run `scraped_data_to_sql` to process and import data into relational database
   - Purpose: Prepare data for web application display and queries

4. **Build the API**

   - Develop REST API endpoints to serve the processed data
   - Enable web application to access and display laptop information

5. **Build the front-end app**
   - Create a user-friendly interface to display laptop data
   - Catch user behavior to give recommend

## Utilities

docker-script.sh: to make a neo4j db

## Run inner files

i.e

```
python -m data_process.process.***
```
