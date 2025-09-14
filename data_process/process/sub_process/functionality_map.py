from rdflib import Graph, Namespace, RDF, RDFS, OWL
import json

# Input/Output files
ontology_file = "data_process/process/owl_outputs/output.owl"  # your ontology file
json_file = "unique_key.json"  # classified mapping
output_file = "data_process/process/owl_outputs/output_new.txt"

# Load ontology
g = Graph()
g.parse(ontology_file, format="turtle")

# Load classification JSON
with open(json_file, "r") as f:
    classified_data = json.load(f)

# Define namespace
BASE = Namespace("http://example.org/ont#")
g.bind("ont", BASE)

# Add satisfiesRequirement property if not in ontology
satisfiesRequirement = BASE.satisfiesRequirement
g.add((satisfiesRequirement, RDF.type, OWL.ObjectProperty))
g.add((satisfiesRequirement, RDFS.domain, BASE.Laptop))
g.add((satisfiesRequirement, RDFS.range, BASE.Functionality))


# Function to map components -> functionalities
def get_functionalities(laptop_components):
    funcs = set()
    for comp in laptop_components:
        for category, items in classified_data.items():
            if comp in items:
                funcs.update(items[comp])
    return funcs


# Iterate laptops
for laptop in g.subjects(RDF.type, BASE.Laptop):
    components = []
    for pred, obj in g.predicate_objects(subject=laptop):
        pred_name = str(pred).split("#")[-1]
        if pred_name.lower().startswith("has"):
            comp_name = str(obj).split("#")[-1]
            components.append(comp_name)

    funcs = get_functionalities(components)
    for f in funcs:
        g.add((laptop, satisfiesRequirement, BASE[f]))

# Save enriched ontology in Turtle format
g.serialize(output_file, format="turtle")
print(f"✅ Enriched ontology saved as {output_file}")
