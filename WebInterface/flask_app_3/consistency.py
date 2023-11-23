import owlready2 as owl
onto = owl.get_ontology("file://trial.owl").load()

def get_epochs(epoch):
    with onto:
        class Hyper_parameters(owl.Thing): 
            pass
        class multiplier(Hyper_parameters >> int, owl.FunctionalProperty): 
            pass
        class current_epoch(Hyper_parameters >> int, owl.FunctionalProperty): 
            pass
        class next_epoch(Hyper_parameters >> int, owl.FunctionalProperty): 
            pass

        rule = owl.Imp()
        rule.set_as_rule("""Hyper_parameters(?d), multiplier(?d, ?p), current_epoch(?d, ?n), multiply(?r, ?p, ?n) -> next_epoch(?d, ?r)""")

    hyp = Hyper_parameters(multiplier = 2, current_epoch = epoch)
    owl.sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
    if len(list(onto.inconsistent_classes())) == 0:
            print("ontology is consistent")
    else:
            print("ontology is incosistent")
    onto.save()

    return hyp.next_epoch