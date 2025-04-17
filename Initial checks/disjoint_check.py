import os
from disjoint_utils import list_disjoint_classes_to_file

if __name__ == "__main__":
    ontology_filename = "dummy.owl"  

    base_dir = os.path.dirname(os.path.abspath(__file__))  
    owl_path = os.path.normpath(os.path.join(base_dir, "..", ontology_filename))
    output_path = os.path.normpath(os.path.join(base_dir, "disjoint_classes.txt"))

    list_disjoint_classes_to_file(owl_path, output_path)
