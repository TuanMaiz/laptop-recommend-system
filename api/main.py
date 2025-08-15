from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from api.routers import laptops

app = FastAPI(title="Laptop Recommendation API")

app.include_router(laptops.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


# Models for request/response
# class LaptopBase(BaseModel):
#     id: str
#     title: str
#     price: float

# class LaptopDetail(LaptopBase):
#     components: dict
#     weight_kg: Optional[float] = None
#     url: Optional[str] = None

# # Get all laptops with pagination
# @app.get("/laptops", response_model=List[LaptopBase])
# def get_all_laptops(skip: int = 0, limit: int = 20):
#     with db.driver.session() as session:
#         result = session.run("""
#         MATCH (l:Resource)
#         WHERE l.uri CONTAINS 'Laptop'
#         OPTIONAL MATCH (l)-[:RELATION {uri: $has_title}]->(title:Resource)
#         OPTIONAL MATCH (l)-[:RELATION {uri: $has_price}]->(price:Resource)
#         RETURN l.uri as id,
#                COALESCE(title.uri, l.uri) as title,
#                toFloat(COALESCE(price.uri, "0")) as price
#         SKIP $skip
#         LIMIT $limit
#         """,
#         has_title="http://www.abacus.ai/ontologies/laptop#hasTitle",
#         has_price="http://www.abacus.ai/ontologies/laptop#hasPrice",
#         skip=skip,
#         limit=limit)

#         return [dict(record) for record in result]

# # Get laptop details by ID
# @app.get("/laptop/{laptop_id}", response_model=LaptopDetail)
# def get_laptop_detail(laptop_id: str):
#     with db.driver.session() as session:
#         result = session.run("""
#         MATCH (l:Resource {uri: $uri})

#         // Get basic properties
#         OPTIONAL MATCH (l)-[:RELATION {uri: $has_title}]->(title:Resource)
#         OPTIONAL MATCH (l)-[:RELATION {uri: $has_price}]->(price:Resource)
#         OPTIONAL MATCH (l)-[:RELATION {uri: $has_weight}]->(weight:Resource)
#         OPTIONAL MATCH (l)-[:RELATION {uri: $has_url}]->(url:Resource)

#         // Get components
#         OPTIONAL MATCH (l)-[:RELATION {uri: $has_component}]->(c:Resource)
#         OPTIONAL MATCH (c)-[:RELATION]->(prop:Resource)

#         WITH l,
#              COALESCE(title.uri, l.uri) as title,
#              toFloat(COALESCE(price.uri, "0")) as price,
#              toFloat(COALESCE(weight.uri, "0")) as weight_kg,
#              COALESCE(url.uri, "") as url,
#              c, collect(distinct {key: type(c), value: prop.uri}) as props

#         RETURN l.uri as id,
#                title,
#                price,
#                weight_kg,
#                url,
#                collect({component: c.uri, properties: props}) as components
#         """,
#         uri=laptop_id,
#         has_title="http://www.abacus.ai/ontologies/laptop#hasTitle",
#         has_price="http://www.abacus.ai/ontologies/laptop#hasPrice",
#         has_weight="http://www.abacus.ai/ontologies/laptop#hasWeightKg",
#         has_url="http://www.abacus.ai/ontologies/laptop#hasUrl",
#         has_component="http://www.abacus.ai/ontologies/laptop#hasComponent")

#         records = list(result)
#         if not records:
#             raise HTTPException(status_code=404, detail="Laptop not found")

#         laptop = dict(records[0])

#         # Format components as a dictionary
#         components_dict = {}
#         for comp in laptop.get("components", []):
#             comp_type = comp["component"].split("#")[-1].split("_")[0]
#             components_dict[comp_type] = {p["key"]: p["value"] for p in comp["properties"]}

#         laptop["components"] = components_dict
#         return laptop

# # Search laptops by criteria
# @app.get("/search", response_model=List[LaptopBase])
# def search_laptops(
#     min_price: Optional[float] = None,
#     max_price: Optional[float] = None,
#     has_dedicated_gpu: Optional[bool] = None,
#     min_ram: Optional[int] = None,
#     query: Optional[str] = None
# ):
#     conditions = []
#     params = {
#         "has_title": "http://www.abacus.ai/ontologies/laptop#hasTitle",
#         "has_price": "http://www.abacus.ai/ontologies/laptop#hasPrice"
#     }

#     # Build query conditions
#     cypher_query = """
#     MATCH (l:Resource)
#     WHERE l.uri CONTAINS 'Laptop'
#     """

#     if min_price is not None:
#         cypher_query += """
#         MATCH (l)-[:RELATION {uri: $has_price}]->(price:Resource)
#         WHERE toFloat(price.uri) >= $min_price
#         """
#         params["min_price"] = min_price

#     if max_price is not None:
#         if "price" not in cypher_query:
#             cypher_query += """
#             MATCH (l)-[:RELATION {uri: $has_price}]->(price:Resource)
#             """
#         cypher_query += "AND toFloat(price.uri) <= $max_price\n"
#         params["max_price"] = max_price

#     if has_dedicated_gpu is not None:
#         cypher_query += """
#         MATCH (l)-[:RELATION {uri: $has_component}]->(gpu:Resource)
#         MATCH (gpu)-[:RELATION {uri: $is_dedicated}]->(dedicated:Resource)
#         WHERE dedicated.uri = $gpu_value
#         """
#         params["has_component"] = "http://www.abacus.ai/ontologies/laptop#hasComponent"
#         params["is_dedicated"] = "http://www.abacus.ai/ontologies/laptop#isDedicatedGpu"
#         params["gpu_value"] = str(has_dedicated_gpu).lower()

#     if min_ram is not None:
#         cypher_query += """
#         MATCH (l)-[:RELATION {uri: $has_component}]->(ram:Resource)
#         MATCH (ram)-[:RELATION {uri: $ram_size}]->(size:Resource)
#         WHERE toInteger(size.uri) >= $min_ram
#         """
#         params["has_component"] = "http://www.abacus.ai/ontologies/laptop#hasComponent"
#         params["ram_size"] = "http://www.abacus.ai/ontologies/laptop#hasRamSizeGB"
#         params["min_ram"] = min_ram

#     if query is not None:
#         cypher_query += """
#         MATCH (l)-[:RELATION {uri: $has_title}]->(title:Resource)
#         WHERE toLower(title.uri) CONTAINS toLower($query)
#         """
#         params["query"] = query

#     # Complete the query
#     cypher_query += """
#     OPTIONAL MATCH (l)-[:RELATION {uri: $has_title}]->(title:Resource)
#     OPTIONAL MATCH (l)-[:RELATION {uri: $has_price}]->(price:Resource)
#     RETURN l.uri as id,
#            COALESCE(title.uri, l.uri) as title,
#            toFloat(COALESCE(price.uri, "0")) as price
#     LIMIT 20
#     """

#     with db.driver.session() as session:
#         result = session.run(cypher_query, **params)
#         return [dict(record) for record in result]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
