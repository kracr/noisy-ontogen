import os
from owlready2 import *

def list_disjoint_classes_to_file(owl_path, output_path):
    onto = get_ontology(owl_path).load()

    disjoint_pairs = set()

    for cls in onto.classes():
        for disjoint_set in cls.disjoints():
            classes = list(disjoint_set.entities)
            for i in range(len(classes)):
                for j in range(i+1, len(classes)):
                    pair = tuple(sorted([classes[i].iri, classes[j].iri]))
                    disjoint_pairs.add(pair)

    with open(output_path, "w") as f:
        for pair in sorted(disjoint_pairs):
            f.write(f"{pair[0]} ⊥ {pair[1]}\n")

    print(f"Saved {len(disjoint_pairs)} disjoint class pairs to '{output_path}'")

