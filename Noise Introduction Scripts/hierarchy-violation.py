import random
from owlready2 import *

# Load the ontology
onto_file_path = input("Enter the path to the OWL file: ").strip()
onto = get_ontology("file://" + onto_file_path).load()
with onto:
    # Collect all subproperty relationships
    subproperty_pairs = []
    for subprop in onto.object_properties():
        for superprop in subprop.is_a:
            if isinstance(superprop, ObjectPropertyClass) and superprop != owl.ObjectProperty:
                subproperty_pairs.append((subprop, superprop))
                print(f"Found subproperty relationship: {subprop.name} ⊑ {superprop.name}")

    print("Number of subproperty relationships:", len(subproperty_pairs))

    if len(subproperty_pairs) == 0:
        print("No subproperty relationships found in the ontology.")
        exit()

    print("""Do you want to introduce noise in the ontology by
        1. Providing a percentage of noise to introduce
        2. Providing the number of hierarchy violations to introduce?
        """)
    method = input("Enter 1 or 2: ").strip()

    if method == "1":
        while True:
            try:
                noise_percentage = float(input("Enter the percentage of noise to introduce (0-100): ").strip())
                if 0 <= noise_percentage <= 100:
                    break
                else:
                    print("Percentage must be between 0 and 100.")
            except ValueError:
                print("Please enter a valid number.")

        num_violations = int(len(subproperty_pairs) * noise_percentage / 100)
        if num_violations == 0 and noise_percentage > 0:
            num_violations = 1
    elif method == "2":
        while True:
            try:
                num_violations = int(input("Enter the number of hierarchy violations to introduce: ").strip())
                if num_violations >= 0:
                    break
            except ValueError:
                print("Please enter a valid number.")
        if num_violations > len(subproperty_pairs):
            num_violations = len(subproperty_pairs)
    else:
        print("Invalid input. Please enter 1 or 2.")
        exit()

    print(f"Generating {num_violations} hierarchy violations...")

    selected_pairs = random.sample(subproperty_pairs, num_violations)
    i = 1

    for subprop, superprop in selected_pairs:
        # Create individuals a and b
        a = Thing(f"a_{i}")
        b = Thing(f"b_{i}")
        subprop[a].append(b)
        disjoint_prop_name = f"Not_{superprop.name}"
        if disjoint_prop_name in onto.object_properties():
            NotSuperprop = onto[disjoint_prop_name]
        else:
            # TODO: Dont create new class, S should be same as that axiom
            # TODO: typeof NotSuperprop should be ObjectProperty
            NotSuperprop = types.new_class(disjoint_prop_name, (ObjectProperty,))
            # Declare disjointness
            # TODO: dont assert both are disjoint, find all pairs of not(S) and assert manually
            # TODO: lookup NegativeObjectPropertyAssertion for this
            # TODO: Should we consider inferred relations or not?
            # TODO: Do reverse lookup, search for papers that cite Box2EL, Owl2Vec, etc.
            AllDisjoint([superprop, NotSuperprop])
            print(f"Created new object property {NotSuperprop.name} disjoint with {superprop.name}")
        NotSuperprop[a].append(b)
        print(f"Asserted {subprop.name}({a.name}, {b.name})")
        i += 1

    print(f"Modified ontology with {num_violations} hierarchy violations")

filename = onto_file_path.split("/")[-1].split(".")[0]
onto.save(file=f"noisy-{filename}-violating-hierarchy.owl", format="rdfxml")
print(f"Modified ontology saved as 'noisy-{filename}-violating-hierarchy.owl'")

noisy_onto = get_ontology("file://" + f"noisy-{filename}-violating-hierarchy.owl").load()

with noisy_onto:
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)