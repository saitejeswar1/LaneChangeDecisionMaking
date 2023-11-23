import rdflib as r


def dq(inArgs,outArgs):
    g = r.Graph()
    g.parse(r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\ltademo.owl',format="ttl")
    outs = []
    qres = g.query("""
        prefix lcs: <http://www.semanticweb.org/saitejeswar/ontologies/2021/2/untitled-ontology-2#> 
        SELECT   ?name ?module

        WHERE 
        { 
        ?subject	lcs:inPar	    "%s";
                    lcs:outPar      "%s";
                    lcs:moduleName  ?module;
                    rdfs:label      ?name.

        }
        """%(inArgs,outArgs))  

   
    for row in qres:
        outs.append(str(row["module"]))
        outs.append(str(row["name"]))
    
    return outs



