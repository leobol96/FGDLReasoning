import os
import common_functions as common
import shutil
import time

if __name__ == "__main__":

    input_ontology = 'datasets/pizza.owl'
    explanation = 'datasets/exp-1.owl'
    signature = 'datasets/signature2.txt'
    inputSubclassStatements = "datasets/subClasses.nt"
    method = '1'
    url_classes = []
    url_to_remove = []

    # Save the explanation
    common.save_explanations(input_ontology, inputSubclassStatements)
    # Get the explanation as string
    exp_string = common.get_string_from_file(explanation)
    # Get the classes and the properties from the ontology
    classes_properties = common.get_classes(input_ontology, False) + common.get_properties(input_ontology, False)

    # For each class in the ontology
    for cla_pro in classes_properties:
        if cla_pro.iri not in exp_string and cla_pro.iri not in url_to_remove:
            url_to_remove.append(cla_pro.iri)

    common.write_signature_to_remove(url_to_remove, signature)
    common.forget_copy_result(input_ontology, method, signature)

    find = True
    while find:
        find = False
        url_classes = []
        url_to_remove = []
        # Remove the classes that are int he explanation but not in the sentence to prove
        input_ontology = 'datasets/result.owl'

        # Save the explanations
        common.save_explanations(input_ontology,inputSubclassStatements)
        # Get the sentence to prove as a string
        sentence_string = common.get_string_from_file(inputSubclassStatements)
        # Get classes and properties from the onology
        classes_properties = common.get_classes(input_ontology, True) + common.get_properties(input_ontology, True)

        # For each class in the ontology
        for cla_pro in classes_properties:
            if cla_pro.iri not in sentence_string and cla_pro.iri not in url_to_remove:
                url_to_remove.append(cla_pro.iri)
                find = True
                break

        common.write_signature_to_remove(url_to_remove, signature)
        common.forget_copy_result(input_ontology, method, signature)
