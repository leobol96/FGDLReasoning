import re
import random
import common_functions as common

def select_signature(prove_file_dir, explanation_dir, input_ontology, heuristic):
    if heuristic == 'min':
        signature = signature_min(input_ontology, prove_file_dir, explanation_dir)
    elif heuristic == 'max':
        signature = signature_max(input_ontology, prove_file_dir, explanation_dir)
    elif heuristic == 'combined_max':
        signature = signature_combined_max(prove_file_dir, explanation_dir)
    else:
        signature = signature_random(input_ontology, prove_file_dir)

    return signature

def signature_random(ontology, prove_file_dir):
    # Get the sentence to prove as a string
    sentence_string = common.get_string_from_file(prove_file_dir)

    # Get the classes and properties from the ontology
    classes_properties = common.get_classes_properties(ontology, True)

    # Filter out all of the items that are not in the explanation
    not_in_sentence = []
    for cla_pro in classes_properties:
        if '<' + cla_pro.iri + '>' not in sentence_string:
            not_in_sentence.append(cla_pro.iri)
    # When there are no items to forget
    if not not_in_sentence:
        return False
    return random.choice(not_in_sentence)

def signature_max(ontology, prove_file_dir, explanation_dir):
    # Get the sentence to prove as a string
    sentence_string = common.get_string_from_file(prove_file_dir)

    # Get the classes and properties from the ontology
    classes_properties = common.get_classes_properties(ontology, True)

    # Get the explanation as a string
    explanation = common.get_string_from_file(explanation_dir)

    count_dict = {}
    for cla_pro in classes_properties:
        if '<' + cla_pro.iri + '>' not in sentence_string:
            count_dict[cla_pro] = explanation.count('<' + cla_pro.iri + '>' )
    # When there are no items to forget
    if not count_dict.keys():
        return False
    max_key = max(count_dict, key=count_dict.get)
    return max_key.iri

def signature_min(ontology, prove_file_dir, explanation_dir):
    # Get the sentence to prove as a string
    sentence_string = common.get_string_from_file(prove_file_dir)

    # Get the classes and properties from the ontology
    classes_properties = common.get_classes_properties(ontology, True)

    # Get the explanation as a string
    explanation = common.get_string_from_file(explanation_dir)

    count_dict = {}
    for cla_pro in classes_properties:
        if '<' + cla_pro.iri + '>' not in sentence_string:
            count_dict[cla_pro] = explanation.count('<' + cla_pro.iri + '>' )
    # When there are no items to forget
    if not count_dict.keys():
        return False
    min_key = min(count_dict, key=count_dict.get)
    return min_key.iri

def signature_combined_max(prove_file_dir, explanation_dir):
    prove_list = prove_to_list(prove_file_dir)
    explanation_list = explanation_to_list(explanation_dir)

    count_dict = {}
    for prove_item in prove_list:
        for axiom in explanation_list:
            if prove_item in axiom:
                for class_expl in axiom:
                    if class_expl not in prove_list:
                        if (prove_item, class_expl) in count_dict.keys():
                            count_dict[(prove_item, class_expl)] += 1
                        else:
                            count_dict[(prove_item, class_expl)] = 1

    if not count_dict.keys():
        return False

    max_key = max(count_dict, key=count_dict.get)
    maximas = max_key[1][1:-1]

    return maximas

def prove_to_list(prove_file_dir):
    """ This function reads the file with the axiom we have to proof and converts it to a list with just the classes (as iri)
    :param proof_file_dir: location of the file with the axiom that we have to prove
    :return:
    """
    # Read the file
    prove = open(prove_file_dir, "r")
    prove_line = prove.readline()

    # Find all classes with regular expression
    prove_list = re.findall('\<.*?\>', prove_line)
    prove.close()

    # return first and last element from list (which are the classes, the middle one is the relation type)
    return prove_list[::len(prove_list)-1]

def explanation_to_list(explanation_dir):
    # Read the file
    explanation = open(explanation_dir)
    temp_explanation = [line for line in explanation]
    explanation.close()

    # Turn the file into a list
    explanation_list = []
    for idx, line in enumerate(temp_explanation):
        if idx == 0 or idx == len(temp_explanation) - 1:
            continue
        explanation_list.append(re.findall('\<.*?\>', line))
    return explanation_list