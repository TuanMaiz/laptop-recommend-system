## Project Plan

This project implements a web scraping and data processing pipeline for laptop data from Sazo website, with both graph database (Neo4j) and relational database (SQL) storage options.

# FastAPI folder structure

api/

├ ── db/

│ ├── session.py # DB connection & Base

│ └── models/

│ └── laptop.py # SQLAlchemy models

├── schemas/

│ └── laptop_schema.py # Pydantic

schemas

├── routers/

│ └── laptops.py # Routes

└── main.py

## Steps

1. **Run scraper to get scraped data** - done

   - Execute the web scraper to collect laptop data from Sazo website
   - Output: sazo_laptop.json file containing structured laptop information

2. **Generate Neo4j Cypher queries** - done
   - Run scraped_data_to_cipher_neo4j to convert scraped data into Cypher queries
   - Purpose: Import data into Neo4j graph database for relationship analysis

3. **Import data into SQL database** - ongoing
   - Run scraped_data_to_sql to process and import data into relational database
   - Purpose: Prepare data for web application display and queries

4. **Build the recommendation engine**
   - Create user interaction tracking system
     - Track clicks, view duration, and search queries
     - Store user-laptop interaction events with timestamps
   - Implement content-based filtering
     - Extract feature vectors from laptop specifications
     - Calculate similarity between laptops based on features
     - Create function to recommend similar laptops
   - Implement collaborative filtering
     - Build user-item interaction matrix
     - Identify similar users based on interaction patterns
     - Recommend laptops popular among similar users
   - Create hybrid recommendation API
     - Combine both filtering approaches with weighted scores
     - Expose endpoints for getting personalized recommendations

   - Run `scraped_data_to_cipher_neo4j` to convert scraped data into Cypher queries
   - Purpose: Import data into Neo4j graph database for relationship analysis

3. **Import data into SQL database** - ongoing

   - Run `scraped_data_to_sql` to process and import data into relational database
   - Purpose: Prepare data for web application display and queries

4. **Build the API**

   - Develop REST API endpoints to serve the processed data
   - Enable web application to access and display laptop information

5. **Build the API layer**
   - Develop REST API endpoints for:
     - Laptop catalog browsing and filtering
     - User profile and interaction history
     - Personalized recommendations
     - Feedback collection on recommendations

6. **Build the front-end app**
   - Create responsive UI for laptop browsing
   - Implement user authentication and profiles
   - Add interaction tracking (clicks, views, purchases)
   - Design recommendation display sections
     - "Similar to what you viewed"
     - "People also bought"
     - "Recommended for you"
   - Add feedback mechanisms for recommendations

7. **Test and optimize the recommendation system**
   - Implement A/B testing framework
   - Measure recommendation effectiveness (CTR, conversion)
   - Tune algorithm weights based on performance
   - Implement continuous learning from user feedback

8. **Deploy and monitor**
   - Set up monitoring for recommendation quality
   - Implement periodic retraining of models
   - Add analytics dashboard for recommendation performance

## Utilities

docker-script.sh: to make a neo4j db

## Run inner files

i.e

```
python -m data_process.process.***
```
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000