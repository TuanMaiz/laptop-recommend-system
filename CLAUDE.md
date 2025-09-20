# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a knowledge-based laptop recommendation system that combines web scraping, semantic web technologies (OWL ontologies), graph databases (Neo4j), relational databases (PostgreSQL), and modern API frameworks (FastAPI) to provide intelligent laptop recommendations.

## Development Commands

### Main API Development
```bash
# Start the FastAPI development server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Run with specific host/port
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Data Processing Pipeline
```bash
# Transform scraped JSON data to OWL ontology
python -m data_process.process.transform_json_to_owl

# Transform scraped data to SQL format
python -m data_process.process.scraped_data_to_sql

# Generate Cypher queries for Neo4j
python -m data_process.process.scraped_data_to_cipher_neo4j

# Populate PostgreSQL database
python -m data_process.populate.populate-postgresql

# Populate Neo4j database
python -m data_process.populate.populate-neo4j
```

### Running Individual Modules
```bash
# Run any module using the -m flag
python -m data_process.***
```

## Architecture Overview

### Core Components

1. **API Layer (FastAPI)**
   - `api/main.py` - Application entry point with CORS middleware
   - `api/routers/` - API endpoints (laptop_router.py, chat_router.py)
   - `api/schemas/` - Pydantic data validation schemas
   - `api/services/` - Business logic and service layer

2. **Data Layer**
   - **PostgreSQL** - Structured laptop data and user interactions
   - **Neo4j** - Graph relationships and semantic reasoning
   - **OWL Ontology** - Semantic representations (api/services/laptop.owl)

3. **Data Pipeline**
   - `data_process/scrape/` - Web scraping from SAZO.vn
   - `data_process/process/` - Data transformation utilities
   - `data_process/populate/` - Database population scripts

4. **Recommendation Engine**
   - Content-based filtering using specifications
   - Collaborative filtering using user interactions
   - Knowledge-based reasoning using semantic relationships

### Key Technology Stack
- **Backend**: FastAPI with Python 3.13+
- **Databases**: PostgreSQL + Neo4j
- **Semantic Web**: RDFLib with OWL ontologies
- **AI/ML**: LangChain, OpenAI integration
- **Package Management**: UV

### Database Models
- **Laptop**: Comprehensive specifications (CPU, RAM, storage, GPU, etc.)
- **User Interaction**: Click tracking, session management
- **Recommendation Preferences**: User profiles and preferences

### OWL Ontology Structure
The ontology defines semantic relationships between:
- Laptop products and specifications
- Component hierarchies (CPU, GPU, RAM types)
- User preferences and use cases
- Performance characteristics and ratings

## Project Structure

```
api/
├── db/              # Database connection and models
├── routers/         # API endpoints
├── schemas/         # Pydantic schemas
├── services/        # Business logic and ontology
data_process/
├── scrape/         # Web scraping
├── process/        # Data transformation
├── populate/       # Database population
utilities/         # Helper functions
```

## Development Workflow

### Environment Setup
- Uses `.env` file for database configuration
- UV for dependency management (modern Python package manager)
- Python 3.13+ required

### Key Files to Understand
- `api/main.py` - FastAPI application setup
- `api/services/laptop_service.py` - Core laptop data access
- `api/services/laptop.owl` - Semantic ontology definitions
- `api/routers/laptop_router.py` - Laptop-related API endpoints

### Data Flow
1. **Scraping** → **JSON Data** → **OWL Ontology** → **PostgreSQL/Neo4j**
2. **API** → **User Interactions** → **Recommendation Engine** → **Personalized Results**

## Configuration

- Database connections configured via `.env` file
- Neo4j default: bolt://localhost:7687
- PostgreSQL configured via environment variables
- OpenAI API key for chatbot functionality

## Recent Development Status

Current branch: `recommendation_services`
- Enhanced ontology files and API services
- Improved recommendation tracking capabilities
- Chatbot integration with OpenAI (in progress)
- User interaction logging and analytics