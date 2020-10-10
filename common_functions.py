import os
import random
import shutil

import owlready2 as ow
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_string_from_file(explanation_file):
    to_return = ''

    with open(explanation_file, 'r') as exp:
        for line in exp:
            to_return += line

    return to_return


def write_signature_to_remove(signature_list, signature_file_name):
    with open(signature_file_name, 'w') as sig_file:
        for idx, signature in enumerate(signature_list):
            if len(signature_list) == idx + 1:
                sig_file.write(signature)
            else:
                sig_file.write(signature + '\n')


def get_classes(ontology, reload):
    """
    This function returns the classes of an ontology
    :param ontology: Ontology to analyze
    :return: List of classes
    """
    onto = ow.get_ontology(ontology)
    onto.load(reload=reload)
    classes = list(onto.classes())
    return classes


def get_properties(ontology, reload):
    """
    This function returns the properties of an ontology
    :param ontology:
    :return:
    """
    onto = ow.get_ontology(ontology)
    onto.load(reload=reload)
    properties = list(onto.properties())

    return properties


def get_rules(ontology, reload):
    """
    This function returns the rules of an ontology
    :param ontology:
    :return:
    """
    onto = ow.get_ontology(ontology)
    onto.load(reload=reload)
    rules = list(onto.rules())

    return rules


def save_subclasses(input_ontology, n_line):
    os.system('java -jar kr_functions.jar ' + 'saveAllSubClasses' + " " + input_ontology)
    to_keep = []

    with open('datasets/subClasses.nt', 'r') as sublasses:
        for idx, sub_class in enumerate(sublasses):
            to_keep.append(sub_class)
            if idx + 1 == n_line:
                break

    with open('datasets/subClasses.nt', 'w') as sublasses:
        for sub_class in to_keep:
            sublasses.write(sub_class)

    return to_keep


def read_sublasses():
    to_return = []
    with open('datasets/subClasses.nt', 'r') as sublasses:
        for line in sublasses:
            to_return.append(line)

    return to_return


def save_explanations(ontology, sub_sentence):
    """
    :param ontology: Ontology where check for the explanations
    :param sub_sentence: Sub sequence for which you want to find the explanation
    """
    os.system('java -jar kr_functions.jar ' + 'saveAllExplanations' + " " + ontology + " " + sub_sentence)


def forget_copy_result(ontology, method, signature_file):
    """
    This function allow to forget some classes from an ontology. Moreover, it copys the result to the dataset folder.
    We did this because the saveAllExplanatins method hase problem with the result.owl if it isn't in the dataset folder.
    :param ontology: Ontology where aply the forget method
    :param method: Method used from the Forgetter
    :param signature_file: File withe the signatures to delete in the ontology
    """
    os.system('java -cp lethe-standalone.jar uk.ac.man.cs.lethe.internal.application.ForgettingConsoleApplication '
              '--owlFile ' + ontology + ' --method ' + method + ' --signature ' + signature_file)
    shutil.copy(os.path.abspath(os.getcwd()) + '/result.owl', os.path.abspath(os.getcwd()) + '/datasets')


def get_element(explanation):
    to_return = []
    string = ''
    open = False
    for char in explanation:

        if char == '<':
            string = ''
            open = True
        elif char == '>':
            if string not in to_return: to_return.append(string)
            open = False
        elif open:
            string += char

    return to_return[1:]


def write_result(result_list):
    """
    This Function write the results in FG_EXPLANATIONS.txt file
    :param result_list: List of explanations
    """
    with open('FG_EXPLANATIONS.txt', 'w') as file:
        for element in result_list:
            file.write(element)
            file.write('\n')

def signature_random(ontology, _, sentence_string):
    # Get the classes and the properties from the ontology
    classes = get_classes(ontology, True)
    props = get_properties(ontology, True)
    classes_properties = classes + props

    # Filter out all of the items that are not in the explanation
    not_in_sentence = []
    for cla_pro in classes_properties:
        if '<' + cla_pro.iri + '>' not in sentence_string:
            not_in_sentence.append(cla_pro.iri)
    # When there are no items to forget
    if not not_in_sentence:
        return False
    return random.choice(not_in_sentence)

def signature_max(ontology, explanation, sentence_string):
    # Get the classes and the properties from the ontology
    classes = get_classes(ontology, True)
    props = get_properties(ontology, True)
    classes_properties = classes + props

    count_dict = {}
    for cla_pro in classes_properties:
        if '<' + cla_pro.iri + '>' not in sentence_string:
            count_dict[cla_pro] = explanation.count('<' + cla_pro.iri + '>' )
    # When there are no items to forget
    if not count_dict.keys():
        return False
    max_key = max(count_dict, key=count_dict.get)
    return max_key.iri


def select_signature(ontology, explanation, sentence, heuristic):
    heuristics = {
        'random': signature_random,
        'max': signature_max
    }

    # Get the classes and the properties from the ontology
    classes = get_classes(ontology, True)
    props = get_properties(ontology, True)
    classes_properties = classes + props

    signature = heuristics[heuristic](ontology, explanation, sentence)

    return signature


def get_list_similarity(strings_list):
    """
    The function return the average of the the cosine similarity between the first element and the others
    Higher is the number returned higher is the similarity between each element of the list.
    The highest returned number is 1, the lowest 0
    :param strings_list: list of element to compare
    :return: Similarity between strings number between 0 and 1
    """

    # Object to convert a list of documents in a matrix of token counts
    co_vec = CountVectorizer()
    # Learn a vocabulary dictionary of all tokens in the raw documents.
    # Transform documents to document-term matrix.
    strings_matrix = co_vec.fit_transform(strings_list)
    # Transform the matrix in array
    strings_matrix = strings_matrix.toarray()
    # Calculate the cosine similarity between each vector in the list
    c_sim = cosine_similarity(strings_matrix)

    return sum(c_sim[0])/len(c_sim)



