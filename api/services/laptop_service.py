import rdflib
from rdflib.namespace import RDF, RDFS
from pathlib import Path
import os
from .recommendation_helper.collab_filtering_service import RDFUSM as USM


class LaptopService:
    def __init__(self, owl_file_path: str = None):
        if owl_file_path is None:
            # Get the directory where this script is located
            # current_dir = os.path.dirname(os.path.abspath(__file__))
            from pathlib import Path

            root_dir = Path(__file__).resolve().parents[2]
            owl_file_path = os.path.join(root_dir, "laptops.owl")
        self.graph = rdflib.Graph()
        self.graph.parse(owl_file_path, format="turtle")

    def get_laptop(self, laptop_id: str):
        """Get laptop details by laptop ID (URI or local name)."""
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?property ?value WHERE {{
            ?laptop ?property ?value .
            FILTER (strends(str(?laptop), "{laptop_id}"))
        }}
        """
        results = self.graph.query(query)
        # print(30*"=")
        # print(results)
        # print(30*"=")
        laptop_data = {}
        for row in results:
            prop = str(row.property)
            val = str(row.value)
            laptop_data[prop] = val
        return laptop_data

    def list_laptop(self, limit=20):
        """List all laptops with their complete specifications and attributes."""
        # First get laptop URIs
        query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX : <http://example.org/laptop#>
        SELECT ?laptop WHERE {{
            ?laptop rdf:type :Product .
        }}
        ORDER BY ?laptop
        LIMIT {limit}
        """
        results = self.graph.query(query)
        laptops = []

        for row in results:
            laptop_uri = str(row.laptop)
            # Extract laptop name from URI
            laptop_name = (
                laptop_uri.split("#")[-1]
                if "#" in laptop_uri
                else laptop_uri.split(":")[-1]
            )

            # Get laptop properties
            laptop_props = {}
            props_query = f"""
            PREFIX : <http://example.org/laptop#>
            SELECT ?prop ?value WHERE {{
                <{laptop_uri}> ?prop ?value .
            }}
            """
            props_results = self.graph.query(props_query)
            for prop_row in props_results:
                prop = str(prop_row.prop)
                value = str(prop_row.value)

                # Clean up property names
                clean_prop = prop.split("#")[-1] if "#" in prop else prop.split(":")[-1]
                clean_value = (
                    value.split("#")[-1]
                    if "#" in value
                    else value.split(":")[-1] if value.startswith("http") else value
                )

                laptop_props[clean_prop] = clean_value

            # Get specifications
            specs_query = f"""
            PREFIX : <http://example.org/laptop#>
            SELECT ?spec ?specType ?specProp ?specValue WHERE {{
                <{laptop_uri}> :hasSpecification ?spec .
                ?spec rdf:type ?specType .
                OPTIONAL {{ ?spec ?specProp ?specValue . }}
            }}
            """
            specs_results = self.graph.query(specs_query)

            specs = {}
            for spec_row in specs_results:
                spec_uri = str(spec_row.spec)
                spec_type = str(spec_row.specType)

                if spec_uri not in specs:
                    spec_name = (
                        spec_uri.split("#")[-1]
                        if "#" in spec_uri
                        else spec_uri.split(":")[-1]
                    )
                    clean_spec_type = (
                        spec_type.split(":")[-1] if ":" in spec_type else spec_type
                    )
                    specs[spec_uri] = {
                        "name": spec_name,
                        "type": clean_spec_type,
                        "properties": {},
                    }

                if hasattr(spec_row, "specProp") and hasattr(spec_row, "specValue"):
                    spec_prop = str(spec_row.specProp)
                    spec_value = str(spec_row.specValue)

                    # Clean up spec property names
                    clean_spec_prop = (
                        spec_prop.split("#")[-1]
                        if "#" in spec_prop
                        else spec_prop.split(":")[-1]
                    )
                    clean_spec_value = (
                        spec_value.split("#")[-1] if "#" in spec_value else spec_value
                    )

                    specs[spec_uri]["properties"][clean_spec_prop] = clean_spec_value

            # Format output
            laptop_info = {
                "name": laptop_name,
                "uri": laptop_uri,
                "properties": laptop_props,
                "specifications": [spec_data for spec_data in specs.values()],
            }
            laptops.append(laptop_info)

        return laptops

    def rate_product(self, fingerprint: str, product_id: str, rating: int):
        root_dir = Path(__file__).resolve().parents[2]
        owl_file_path = os.path.join(root_dir, "laptops.owl")

        try:
            usm = USM(owl_file_path)
            usm.rate_product(
                fingerprint,
                product_id,
                rating,
            )
            return True
        except Exception as e:
            print(f"Error rating product: {e}")
            return False
