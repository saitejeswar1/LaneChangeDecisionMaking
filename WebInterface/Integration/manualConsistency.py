import rdflib as r


g = r.Graph()
g.parse(r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\ltademo.owl', format="ttl")

qres = g.query("""  PREFIX lcs: <http://www.semanticweb.org/saitejeswar/ontologies/2021/2/untitled-ontology-2#>
                    SELECT  ?objects ?object
                    WHERE {
                            lcs:ambulance rdf:type      ?object.
                            ?object       rdfs:label    ?objects.
                            }
                    """)
classes = []

for row in qres:
    classes.append(str(row["objects"]))
print(classes)
qres1 = g.query(""" PREFIX lcs: <http://www.semanticweb.org/saitejeswar/ontologies/2021/2/untitled-ontology-2#>
                    SELECT  ?object1 ?object2
                    WHERE {
                            ?object1 rdfs:label "%s".
                            ?object2 rdfs:label "%s".
                            ?object1 owl:disjointWith ?object2.
                            }
                    """%(classes[1],classes[0]))

for row in qres1:
    print("inconsistent")


