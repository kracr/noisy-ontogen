#!/usr/bin/env python
import sys
import os
from rdflib import Graph, Namespace, BNode, URIRef

# Define common namespaces.
RDF   = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS  = Namespace("http://www.w3.org/2000/01/rdf-schema#")
OWL   = Namespace("http://www.w3.org/2002/07/owl#")

def add_negative_property_assertion(g, prop, subj, obj):
    """
    Adds a negative property assertion (NPA) to the graph.
    """
    npa = BNode()
    g.add((npa, RDF.type, OWL.NegativePropertyAssertion))
    g.add((npa, OWL.sourceIndividual, subj))
    g.add((npa, OWL.assertionProperty, prop))
    g.add((npa, OWL.targetIndividual, obj))

def main():
    if len(sys.argv) < 2:
        print("Usage: python make_role_comp_inconsistent.py <ontology.owl>")
        sys.exit(1)

    ontology_path = sys.argv[1]
    abs_path = os.path.abspath(ontology_path)
    
    # Load the ontology.
    g = Graph()
    g.parse(abs_path, format="xml")  # assumes RDF/XML format

    # STEP 1: Find all role composition axioms of the form: owl:propertyChainAxiom [R1, R2] ⊑ S
    role_compositions = []
    for s, p, o in g.triples((None, OWL.propertyChainAxiom, None)):
        # `o` is a RDF list of properties
        chain_list = []
        while (o != RDF.nil):
            first = g.value(o, RDF.first)
            if first:
                chain_list.append(first)
            o = g.value(o, RDF.rest)
        if len(chain_list) == 2:
            role_compositions.append((chain_list[0], chain_list[1], s))

    print(f"Found {len(role_compositions)} role composition axioms.")

    # STEP 2: For each role composition (R1, R2 ⊑ S), find a, b, c such that:
    # R1(a, b) and R2(b, c), and then add ¬S(a, c)
    for R1, R2, S in role_compositions:
        count = 0
        for a, _, b in g.triples((None, R1, None)):
            for b2, _, c in g.triples((b, R2, None)):
                if b2 == b:  # match the shared middle entity
                    add_negative_property_assertion(g, S, a, c)
                    count += 1
        print(f"Inserted {count} violations for composition {R1} o {R2} ⊑ {S}")

    # STEP 3: Save the noisy ontology
    base_name = os.path.basename(ontology_path)
    output_path = os.path.join(os.path.dirname(ontology_path), "noisy_composition_" + base_name)
    g.serialize(destination=output_path, format="xml")
    print(f"Noisy ontology saved as {output_path}")

if __name__ == "__main__":
    main()
