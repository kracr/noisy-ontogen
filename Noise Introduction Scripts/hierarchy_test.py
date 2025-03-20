# create_dummy_ontology.py
from owlready2 import get_ontology, Thing, ObjectProperty

# Create a new ontology with a base IRI
onto = get_ontology("http://example.org/dummy.owl")

with onto:
    # Define a dummy class to use if needed
    class Dummy(Thing):
        pass

    # Define two object properties: R and S
    class R(ObjectProperty):
        pass

    class S(ObjectProperty):
        pass

    # Assert that R is a subproperty of S (i.e., R ⊆ S)
    R.is_a.append(S)

    # Create sample individuals
    a = Dummy("a")
    b = Dummy("b")
    c = Dummy("c")
    d = Dummy("d")

    # Assert that individual 'a' is related to 'b' by property R
    a.R.append(b)

    # Assert that individual 'c' is related to 'd' by property S
    c.S.append(d)

# Save the ontology to an OWL file in RDF/XML format
onto.save(file="dummy.owl", format="rdfxml")
print("Ontology saved as dummy.owl")
