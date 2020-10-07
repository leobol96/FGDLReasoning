import os
import shutil

import owlready2 as ow


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