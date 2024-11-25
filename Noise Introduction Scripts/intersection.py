from owlready2 import *
import random

# Input: Path to the ontology
inp = input("Enter the path to the ontology: ")

# Load your ontology
onto = get_ontology(inp).load()

# List to store intersection classes
intersection_classes = []

# Iterate through all classes in the ontology
for cls in onto.classes():
    # Check if the class has equivalent_to axioms
    for eq in cls.equivalent_to:
        # Check if the axiom is an intersection (AND) of two classes
        if isinstance(eq, And) and len(eq.Classes) == 2:
            class1, class2 = eq.Classes  # Get the two classes involved in the intersection
            intersection_classes.append((cls, class1, class2))

for i in intersection_classes:
    print(i)

# Input: Number of intersection classes to introduce noise in
n = int(input("Enter the number of intersection classes to introduce noise in: "))

# Ensure the number of noisy entities is valid
if n > len(intersection_classes):
    print("Error: More noise entities requested than available intersections.")
    exit()

# Randomly sample from intersection_classes
intersection_classes_to_noise = random.sample(intersection_classes, n)

# Introduce noise in the selected intersection classes
for cls, class1, class2 in intersection_classes_to_noise:
    # Create a unique noise entity
    noise_entity_name = f"NoiseEntity_{random.randint(1000, 9999)}"
    noise_entity = Thing(name=noise_entity_name, namespace=onto)

    # Add assertions to the noise entity
    noise_entity.is_a.append(cls)
    noise_entity.is_a.append(Not(class1))
    noise_entity.is_a.append(Not(class2))

# Save the modified ontology
output_path = "intersection_noise.owl"
onto.save(file=output_path, format="rdfxml")

print(f"Modified ontology saved to {output_path}")
