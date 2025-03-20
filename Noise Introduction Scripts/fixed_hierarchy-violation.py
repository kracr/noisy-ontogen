#!/usr/bin/env python
import sys
import os
from rdflib import Graph, Namespace, BNode

# Define common namespaces.
RDF   = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS  = Namespace("http://www.w3.org/2000/01/rdf-schema#")
OWL   = Namespace("http://www.w3.org/2002/07/owl#")

def add_negative_property_assertion(g, prop, subj, obj):
    """
    Adds a negative property assertion (NPA) to the graph.
    This creates a blank node representing:
      _:npa rdf:type owl:NegativePropertyAssertion .
      _:npa owl:sourceIndividual subj .
      _:npa owl:assertionProperty prop .
      _:npa owl:targetIndividual obj .
    """
    npa = BNode()
    g.add((npa, RDF.type, OWL.NegativePropertyAssertion))
    g.add((npa, OWL.sourceIndividual, subj))
    g.add((npa, OWL.assertionProperty, prop))
    g.add((npa, OWL.targetIndividual, obj))

def main():
    if len(sys.argv) < 2:
        print("Usage: python make_noisy_rdflib.py <ontology.owl>")
        sys.exit(1)

    ontology_path = sys.argv[1]
    abs_path = os.path.abspath(ontology_path)
    
    # Load the ontology.
    g = Graph()
    g.parse(abs_path, format="xml")  # assuming the input is in RDF/XML format

    # CHANGE: Find all subproperty pairs: for every triple (R, rdfs:subPropertyOf, S)
    subproperty_pairs = []
    for R, _, S in g.triples((None, RDFS.subPropertyOf, None)):
        subproperty_pairs.append((R, S))
    
    # For each subproperty pair (R, S), find all triples (subject, R, object)
    # and add a negative property assertion for S.
    for R, S in subproperty_pairs:
        for subj, _, obj in g.triples((None, R, None)):
            add_negative_property_assertion(g, S, subj, obj)

    # Save the modified ontology with a new name "noisy_<original_name>.owl"
    base_name = os.path.basename(ontology_path)
    output_path = os.path.join(os.path.dirname(ontology_path), "noisy_" + base_name)
    g.serialize(destination=output_path, format="xml")
    print(f"Ontology saved as {output_path}")

if __name__ == "__main__":
    main()
