from owlready2 import *
import random

class IntersectionNoiseGenerator:
    def __init__(self, ontology_path):
        self.ontology_path = ontology_path
        self.onto = get_ontology(ontology_path).load()
        self.intersection_classes = []

    def find_intersection_classes(self):
        for cls in self.onto.classes():
            for eq in cls.equivalent_to:
                if isinstance(eq, And) and len(eq.Classes) == 2:
                    class1, class2 = eq.Classes
                    self.intersection_classes.append((cls, class1, class2))

    def introduce_noise(self, n):
        if n > len(self.intersection_classes):
            raise ValueError("More noise entities requested than available intersections.")
        
        intersection_classes_to_noise = random.sample(self.intersection_classes, n)
        
        for cls, class1, class2 in intersection_classes_to_noise:
            noise_entity_name = f"NoiseEntity_{random.randint(1000, 9999)}"
            noise_entity = Thing(name=noise_entity_name, namespace=self.onto)
            noise_entity.is_a.append(cls)
            noise_entity.is_a.append(Not(class1))
            noise_entity.is_a.append(Not(class2))

    def save_ontology(self, output_path):
        self.onto.save(file=output_path, format="rdfxml")
        print(f"Modified ontology saved to {output_path}")
 
if __name__ == "__main__":
    ontology_path = input("Enter the path to the ontology: ")
    generator = IntersectionNoiseGenerator(ontology_path)
    generator.find_intersection_classes()
    
    for i in generator.intersection_classes:
        print(i)
    
    n = int(input("Enter the number of intersection classes to introduce noise in: "))
    try:
        generator.introduce_noise(n)
        generator.save_ontology("intersection_noise.owl")
    except ValueError as e:
        print(e)
