from noisyOntoGen import IntersectionNoiseGeneratorFactory
import os

generator = IntersectionNoiseGeneratorFactory(
    ontology_path='./pizza.owl'
  )

generator.find_intersection_classes()
n = generator.getNoiseSetSize()
current_dir = os.getcwd()

generator.introduce_noise(n)
generator.save_ontology(current_dir + '/pizza_modified.owl')

# Alternate method
generator.generate(100, current_dir + '/pizza_modified.owl')