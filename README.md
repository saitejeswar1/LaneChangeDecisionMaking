# LaneChangeDecisionMaking
 
-	A knowledge base with various road topologies was created to support the ANN.
-	The Knowledge Base (KB) could infer the logged data, create rules, and store them for future use.
-	The inconsistencies, if any, in the KB are detected using the Python library by making queries in RDF.
-	Instance segmentation was used to detect various classes of objects in the videos.
-	Developed a Python API running MATLAB engine to detect lane boundaries.
-	Created an ML pipeline of the above-mentioned functions using FLASK as a web application.


# Introduction

Knowledge engineering (KE) refers to all technical, scientific, and social aspects involved in building, maintaining, and using knowledge-based systems [1]. Knowledge engineers work to convert human expertise into what is known as a knowledge-based machine, which can mimic someone's response. These systems are used to solve complicated, high-level challenges that would otherwise need the assistance of a business specialist. Knowledge engineering has evolved because of emerging technologies such as cloud computing services, which  demand vast volumes of data. In this project a Knowledge Base is used in addition to Artificial Neural Networks to replicate a human thinking while making the decision to change lanes in an autonomous vehicle on freeways. In simple terms, Knowledge Base is a set of instructions, and/or rules and/or decisions in certain conditions which are generally written using Resource Description Framework (RDF). The Knowledge Base is written using Turtle syntax[2]. OWL[3] and SWRL[4] are the ontology languages used to develop the Knowledge Base and SPARQL is used for querying the same. A web app interface is used to view the various parts of the project which includes documentation, ontology, Neural Network training and an option to test the KBANN which makes the decision for Lane changing. The scope of this project remains to assist the driver to take a decision in a situation where there is a need for lane changing while driving on freeway. The output of the decision can be used to control the Car to perform the action of Lane changing in case of Level-3 or more autonomous vehicles, but this is beyond the scope of this project. 
