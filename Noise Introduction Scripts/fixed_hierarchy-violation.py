# introduce_inconsistency.py
import sys
from rdflib import Graph, Namespace, BNode, RDF, URIRef

if len(sys.argv) < 2:
    print("Usage: python introduce_inconsistency.py <ontology.owl>")
    sys.exit(1)

# Load the input ontology (assumed to be in RDF/XML format)
input_file = sys.argv[1]
g = Graph()
g.parse(input_file, format="xml")

# Define namespaces
EX = Namespace("http://example.org/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")

g.bind("ex", EX)
g.bind("rdfs", RDFS)
g.bind("owl", OWL)

# Counter to generate unique individual names per R-S pair
counter = 1

# Find all property pairs (r, s) where r is a subproperty of s
for r, _, s in g.triples((None, RDFS.subPropertyOf, None)):
    # Create new individuals for the inconsistency tuple.
    # We derive local names (if possible) from the property URIs.
    r_local = str(r).split('#')[-1] if '#' in str(r) else str(r).split('/')[-1]
    s_local = str(s).split('#')[-1] if '#' in str(s) else str(s).split('/')[-1]
    
    subj = URIRef(EX[f"inc_subject_{counter}_{r_local}"])
    obj  = URIRef(EX[f"inc_object_{counter}_{r_local}"])
    
    # Add the positive assertion: (subj, r, obj)
    g.add((subj, r, obj))
    
    # Create a blank node for the negative property assertion for s.
    neg = BNode()
    g.add((neg, RDF.type, OWL.NegativePropertyAssertion))
    g.add((neg, OWL.sourceIndividual, subj))
    g.add((neg, OWL.assertionProperty, s))
    g.add((neg, OWL.targetIndividual, obj))
    
    print(f"Introduced inconsistency for property pair: {r_local} ⊆ {s_local}")
    counter += 1

# Save the modified ontology to a new file.
output_file = "inconsistent.owl"
g.serialize(destination=output_file, format="xml")
print(f"Inconsistent ontology saved as {output_file}")
