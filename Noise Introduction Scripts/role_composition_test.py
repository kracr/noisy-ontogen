from owlready2 import get_ontology, Thing, ObjectProperty, Not
from rdflib import Namespace, RDF, OWL, URIRef, BNode, Graph

# Step 1: Create base ontology using Owlready2
onto = get_ontology("http://example.org/role_comp_dummy.owl")

with onto:
    class Student(Thing): pass
    class Course(Thing): pass

    class EnrolledIn(ObjectProperty): pass
    class PrerequisiteOf(ObjectProperty): pass
    class Completed(ObjectProperty): pass

    EnrolledIn.domain = [Student]
    EnrolledIn.range = [Course]

    PrerequisiteOf.domain = [Course]
    PrerequisiteOf.range = [Course]

    Completed.domain = [Student]
    Completed.range = [Course]

    # Individuals
    alice = Student("Alice")
    math101 = Course("Math101")
    math102 = Course("Math102")

    alice.EnrolledIn.append(math101)
    math101.PrerequisiteOf.append(math102)

    # Add ¬Completed(Alice, Math102)
    alice.is_a.append(Not(Completed.value(math102)))

# Save base ontology
base_path = "role_composition_dummy.owl"
onto.save(file=base_path, format="rdfxml")
print("Base ontology saved as", base_path)

# Step 2: Inject role composition axiom with rdflib
g = Graph()
g.parse(base_path, format="xml")

EX = Namespace("http://example.org/role_comp_dummy.owl#")
g.bind("ex", EX)

# Create RDF list: (EnrolledIn PrerequisiteOf)
list_node1 = BNode()
list_node2 = BNode()

g.add((EX.Completed, OWL.propertyChainAxiom, list_node1))
g.add((list_node1, RDF.first, EX.EnrolledIn))
g.add((list_node1, RDF.rest, list_node2))
g.add((list_node2, RDF.first, EX.PrerequisiteOf))
g.add((list_node2, RDF.rest, RDF.nil))

# Save updated ontology
updated_path = "role_composition_dummy_with_chain.owl"
g.serialize(destination=updated_path, format="xml")
print("Updated ontology saved as", updated_path)

