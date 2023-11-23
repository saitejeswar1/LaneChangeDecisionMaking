from owlready2 import *

inferences = get_ontology("file://ltademo.owl").load()

with inferences:
   sync_reasoner()

inferences.save("trial1.owl")

