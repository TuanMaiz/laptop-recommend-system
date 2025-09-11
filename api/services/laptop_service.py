
import rdflib
from rdflib.namespace import RDF, RDFS
import os

class LaptopService:
    def __init__(self, owl_file_path: str = None):
        if owl_file_path is None:
            # Get the directory where this script is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            owl_file_path = os.path.join(current_dir, "laptop.owl")
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
        print(30*"=")
        print(results)
        print(30*"=")
        laptop_data = {}
        for row in results:
            prop = str(row.property)
            val = str(row.value)
            laptop_data[prop] = val
        return laptop_data

    def list_laptop(self):
        """List all laptops in the ontology."""
        query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?laptop WHERE {
            ?laptop rdf:type ?type .
            FILTER regex(str(?type), "Laptop", "i")
        }
        """
        results = self.graph.query(query)
        laptops = [str(row.laptop) for row in results]
        return laptops