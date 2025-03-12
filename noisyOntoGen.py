from owlready2 import *
import random

class IntersectionNoiseGeneratorFactory:
    """A class to generate noise in ontology intersections.
    This class introduces noise in ontological intersections by creating entities that
    belong to an intersection class but explicitly do not belong to its constituent classes,
    thereby creating logical inconsistencies.
    Parameters
    ----------
    ontology_path : str
      File path to the input ontology
    Methods
    -------
    find_intersection_classes()
      Identifies all intersection classes in the ontology
    introduce_noise(n)
      Creates n noise entities that violate intersection axioms
    save_ontology(output_path)
      Saves the modified ontology to the specified path
    generate(percentage, output_path)
      Main method to generate noise based on percentage of intersections
    Attributes
    ----------
    ontology_path : str
      Path to the input ontology file
    onto : owlready2.Ontology
      Loaded ontology object
    intersection_classes : list
      List of tuples containing (intersection_class, class1, class2)
    """
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

    def getNoiseSetSize(self):
        return len(self.intersection_classes)

    def save_ontology(self, output_path):
        self.onto.save(file=output_path, format="rdfxml")
        print(f"Modified ontology saved to {output_path}")

    def generate(self, percentage, output_path):
        self.find_intersection_classes()
        n = (percentage / 100) * len(self.intersection_classes)
        
        self.introduce_noise(n)
        self.save_ontology()

 
if __name__ == "__main__":
    ontology_path = input("Enter the path to the ontology: ")
    generator = IntersectionNoiseGeneratorFactory(ontology_path)
    generator.find_intersection_classes()
    
    for i in generator.intersection_classes:
        print(i)
    
    n = int(input("Enter the number of intersection classes to introduce noise in: "))
    try:
        generator.introduce_noise(n)
        generator.save_ontology("intersection_noise.owl")
    except ValueError as e:
        print(e)
