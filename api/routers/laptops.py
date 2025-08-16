from fastapi import APIRouter

router = APIRouter()


# Get all laptops with pagination
@router.get("/laptops", response_model=List[LaptopBase])
async def get_all_laptops(skip: int = 0, limit: int = 20):
    # with db.driver.session() as session:
    #     result = session.run(
    #         """
    #     MATCH (l:Resource)
    #     WHERE l.uri CONTAINS 'Laptop'
    #     OPTIONAL MATCH (l)-[:RELATION {uri: $has_title}]->(title:Resource)
    #     OPTIONAL MATCH (l)-[:RELATION {uri: $has_price}]->(price:Resource)
    #     RETURN l.uri as id,
    #            COALESCE(title.uri, l.uri) as title,
    #            toFloat(COALESCE(price.uri, "0")) as price
    #     SKIP $skip
    #     LIMIT $limit
    #     """,
    #         has_title="http://www.abacus.ai/ontologies/laptop#hasTitle",
    #         has_price="http://www.abacus.ai/ontologies/laptop#hasPrice",
    #         skip=skip,
    #         limit=limit,
    #     )

    return [dict(record) for record in result]


# Get laptop details by ID
@router.get("/laptop/{laptop_id}", response_model=LaptopDetail)
def get_laptop_detail(laptop_id: str):
    with db.driver.session() as session:
        result = session.run(
            """
        MATCH (l:Resource {uri: $uri})
        
        // Get basic properties
        OPTIONAL MATCH (l)-[:RELATION {uri: $has_title}]->(title:Resource)
        OPTIONAL MATCH (l)-[:RELATION {uri: $has_price}]->(price:Resource)
        OPTIONAL MATCH (l)-[:RELATION {uri: $has_weight}]->(weight:Resource)
        OPTIONAL MATCH (l)-[:RELATION {uri: $has_url}]->(url:Resource)
        
        // Get components
        OPTIONAL MATCH (l)-[:RELATION {uri: $has_component}]->(c:Resource)
        OPTIONAL MATCH (c)-[:RELATION]->(prop:Resource)
        
        WITH l, 
             COALESCE(title.uri, l.uri) as title,
             toFloat(COALESCE(price.uri, "0")) as price,
             toFloat(COALESCE(weight.uri, "0")) as weight_kg,
             COALESCE(url.uri, "") as url,
             c, collect(distinct {key: type(c), value: prop.uri}) as props
        
        RETURN l.uri as id, 
               title,
               price,
               weight_kg,
               url,
               collect({component: c.uri, properties: props}) as components
        """,
            uri=laptop_id,
            has_title="http://www.abacus.ai/ontologies/laptop#hasTitle",
            has_price="http://www.abacus.ai/ontologies/laptop#hasPrice",
            has_weight="http://www.abacus.ai/ontologies/laptop#hasWeightKg",
            has_url="http://www.abacus.ai/ontologies/laptop#hasUrl",
            has_component="http://www.abacus.ai/ontologies/laptop#hasComponent",
        )

        records = list(result)
        if not records:
            raise HTTPException(status_code=404, detail="Laptop not found")

        laptop = dict(records[0])

        # Format components as a dictionary
        components_dict = {}
        for comp in laptop.get("components", []):
            comp_type = comp["component"].split("#")[-1].split("_")[0]
            components_dict[comp_type] = {
                p["key"]: p["value"] for p in comp["properties"]
            }

        laptop["components"] = components_dict
        return laptop
