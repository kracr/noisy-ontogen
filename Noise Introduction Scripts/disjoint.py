import random
from owlready2 import *

onto_file_path = input("Enter the path to the OWL file: ")
onto = get_ontology("file://" + onto_file_path).load()

disjoint_pairs = set()
for disjoint_axiom in onto.disjoint_classes():
    classes = set(disjoint_axiom.entities)
    disjoint_pairs.add(frozenset(classes))

disjoint_pairs = list(disjoint_pairs)
disjoint_pairs = [list(pair) for pair in disjoint_pairs]

print("Disjoint Class Axioms:")
print(disjoint_pairs)
print("Number of disjoint class pairs:", len(disjoint_pairs))

print("""Do you want to introduce noise in the ontology by 
      1. Providing a percentage of noise to introduce 
      2. Providing the number of non-disjoint axioms to introduce?
      """)

method = input("Enter 1 or 2: ")

if method == "1":
    while True:
        try:
            noise_percentage = float(input("Enter the percentage of noise to introduce (0-100): "))
            if 0 <= noise_percentage <= 100:
                break
            else:
                print("Percentage must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")

    num_non_disjoint_axioms = int(len(disjoint_pairs) * noise_percentage / 100) + 1
    if num_non_disjoint_axioms > len(disjoint_pairs):
        num_non_disjoint_axioms = len(disjoint_pairs)

elif method == "2":
    while True:
        try:
            num_non_disjoint_axioms = int(input("Enter the number of non-disjoint axioms to introduce: "))
            if num_non_disjoint_axioms > 0:
                break
        except ValueError:
            print("Please enter a valid number.")
    

print("Generating", num_non_disjoint_axioms, "non-disjoint axioms...")

i = 1

for _ in range(num_non_disjoint_axioms):
    chosen_pair = random.choice(disjoint_pairs)
    print("Chosen pair:", chosen_pair)

    class_a_name, class_b_name, *sink = chosen_pair

    ClassA = class_a_name
    ClassB = class_b_name

    class_a_name = class_a_name.name
    class_b_name = class_b_name.name
    print("class_a_name: ", class_a_name)
    print("class_b_name: ", class_b_name)

    print("ClassA:", ClassA)
    print("ClassB:", ClassB)

    individual_a = ClassA(f"individual_{i}")
    individual_b = ClassB(f"individual_{i+1}")
    individual_b = ClassA(f"individual_{i+1}")
    i += 2

    individual_a_classes = individual_a.is_a
    individual_b_classes = individual_b.is_a
    print("Individual A Classes:", individual_a_classes)
    print("Individual B Classes:", individual_b_classes)

    print("Individual A:", individual_a)
    print("Individual B:", individual_b)

filename = onto.base_iri.split("/")[-1].split(".")[0]

onto.save(file=f"noisy-disjoint.owl", format="rdfxml")

print("Modified ontology saved as 'noisy-disjoint.owl'")

noisy_onto = get_ontology("file://" + f"noisy-disjoint.owl").load()

with noisy_onto:
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
