import random
from owlready2 import *

# Load the ontology
onto_file_path = input("Enter the path to the OWL file: ").strip()
onto = get_ontology("file://" + onto_file_path).load()

with onto:
    # Collect all equivalence relationships
    equivalence_pairs = []
    for cls in onto.classes():
        for equiv_cls in cls.equivalent_to:
            if isinstance(equiv_cls, ThingClass) or isinstance(equiv_cls, (And, Or)):
                equivalence_pairs.append((cls, equiv_cls))
                print(f"Found equivalence relationship: {cls.name} ≡ {equiv_cls}")

    print("Number of equivalence relationships:", len(equivalence_pairs))

    if len(equivalence_pairs) == 0:
        print("No equivalence relationships found in the ontology.")
        exit()

    print("""Do you want to introduce noise in the ontology by
        1. Providing a percentage of noise to introduce
        2. Providing the number of equivalence violations to introduce?
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

        num_violations = int(len(equivalence_pairs) * noise_percentage / 100)
        if num_violations == 0 and noise_percentage > 0:
            num_violations = 1
    elif method == "2":
        while True:
            try:
                num_violations = int(input("Enter the number of equivalence violations to introduce: ").strip())
                if num_violations >= 0:
                    break
            except ValueError:
                print("Please enter a valid number.")
        if num_violations > len(equivalence_pairs):
            num_violations = len(equivalence_pairs)
    else:
        print("Invalid input. Please enter 1 or 2.")
        exit()

    print(f"Generating {num_violations} equivalence violations...")

    selected_pairs = random.sample(equivalence_pairs, num_violations)
    i = 1

    for cls, equiv_cls in selected_pairs:
        # Create an individual
        individual = Thing(f"individual_{i}")
        individual.is_a.append(cls)

        # Introduce noise by asserting ¬equiv_cls for the same individual
        if isinstance(equiv_cls, (And, Or)):
            # Handle complex expressions
            equiv_description = " & ".join([sub.name if isinstance(sub, ThingClass) else str(sub) for sub in equiv_cls.Classes])
            individual.is_a.append(Not(equiv_cls))
            print(f"Introduced violation: {cls.name}({individual.name}), ¬({equiv_description})({individual.name})")
        else:
            # Handle simple equivalence relationships
            individual.is_a.append(Not(equiv_cls))
            print(f"Introduced violation: {cls.name}({individual.name}), ¬{equiv_cls.name}({individual.name})")
        i += 1

    print(f"Modified ontology with {num_violations} equivalence violations")

filename = onto_file_path.split("/")[-1].split(".")[0]
onto.save(file=f"noisy-{filename}-violating-equivalence.owl", format="rdfxml")
print(f"Modified ontology saved as 'noisy-{filename}-violating-equivalence.owl'")

noisy_onto = get_ontology("file://" + f"noisy-{filename}-violating-equivalence.owl").load()

with noisy_onto:
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
