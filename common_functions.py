import os
import shutil

import matplotlib.pyplot as plt
import numpy as np
import owlready2 as ow
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_string_from_file(explanation_file):
    """
    The function returns a file as a string
    :param explanation_file: File to read
    :return: String that represents the file read
    """
    to_return = ''

    with open(explanation_file, 'r') as exp:
        for line in exp:
            to_return += line

    return to_return


def write_signature_to_remove(signature_list, signature_file_name):
    """
    The function writes a list of signatures in a file. This file will be used to delete the signatures from the ontology
    :param signature_list: Signature or list of signatures to write in the file.
    :param signature_file_name: Name of the file where write the signatures
    """
    with open(signature_file_name, 'w') as sig_file:
        for idx, signature in enumerate(signature_list):
            if len(signature_list) == idx + 1:
                sig_file.write(signature)
            else:
                sig_file.write(signature + '\n')


def get_classes_properties(ontology, reload):
    """
    This function returns the classes and the properties in a ontology
    :param ontology: Ontology to analyze
    :return: List of classes and properties
    """
    onto = ow.get_ontology(ontology)
    onto.load(reload=reload)
    classes = list(onto.classes())
    properties = list(onto.object_properties())
    return classes + properties


def save_subclasses(input_ontology, n_line):
    """
    The function saves N subclasses relationship from a specific ontology.
    The subclasses will be saved in the file subClasses.nt
    :param input_ontology: Ontology to analyze.
    :param n_line: Number of relationship that one wants to save.
    :return: List of relationships saved in the file.
    """
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
    """
    This function reads the subclasses in the file subClasses.nt
    :return: A list of subclasses present in the file.
    """
    to_return = []
    with open('datasets/subClasses.nt', 'r') as sublasses:
        for line in sublasses:
            to_return.append(line)

    return to_return


def save_explanations(ontology, sub_sentence):
    """
    The functions save a set of explanations. The explanations are for each relationship present in sub_sentence file
    using the ontology passed as parameter.
    :param ontology: Ontology where check for the explanations
    :param sub_sentence: Sub sequence for which you want to find the explanation
    """
    os.system('java -jar kr_functions.jar ' + 'saveAllExplanations' + " " + ontology + " " + sub_sentence)


def forget_copy_result(ontology, method, signature_file):
    """
    This function allow to forget some classes and properties from an ontology. Moreover, it copies the result to the dataset folder.
    The copy of the file has been done because the saveAllExplanatins method hase problem with the result.owl if it isn't in the dataset folder.
    :param ontology: Ontology where aply the forget method
    :param method: Method used from the Forgetter
    :param signature_file: File withe the signatures to delete in the ontology
    """
    os.system('java -cp lethe-standalone.jar uk.ac.man.cs.lethe.internal.application.ForgettingConsoleApplication '
              '--owlFile ' + ontology + ' --method ' + method + ' --signature ' + signature_file)
    shutil.copy(os.path.abspath(os.getcwd()) + '/result.owl', os.path.abspath(os.getcwd()) + '/datasets')


def write_result(result_list):
    """
    This Function write the results of the forgetting reasoning in FG_EXPLANATIONS.txt file
    :param result_list: List of explanations
    """
    with open('FG_EXPLANATIONS.txt', 'w') as file:
        for element in result_list:
            file.write(element)
            file.write('\n')


def check_error_proof(to_proof, error_file):
    """
    The function checks if there are present any errors in the proof
    :param to_proof: thing we want to proof
    :return: true if the proof is known to give an error false otherwise
    """
    error_file = open(error_file, 'r')
    error_proofs = error_file.readlines()
    if to_proof in error_proofs:
        return True
    return False

    # Get the classes and the properties from the ontology
    classes = get_classes(ontology, True)
    props = get_properties(ontology, True)
    classes_properties = classes + props

    signature = heuristics[heuristic](ontology, explanation, sentence)

    return signature


def get_list_similarity(strings_list):
    """
    The function return the average of the the cosine similarity between the first element and the others
    Higher is the number returned higher is the difference between each explanation of the list.
    The highest returned number is 1, the lowest 0. Moreover it returns the value of cosine similarity for each step
    and the number of chars deleted for each step.
    :param List of explanations
    :return:
        Average of difference for each step, list with the differences for each step, list of deleted char for each step

    """

    # Object to convert a list of documents in a matrix of token counts
    co_vec = CountVectorizer()
    # List containing a value that represent the similarity between each step
    change_by_step = []
    # List of number of word deleted for each step
    deleted_chars_by_step = []

    for idx_element in range(0, len(strings_list) - 1):
        string_to_compare = [strings_list[idx_element], strings_list[idx_element + 1]]
        deleted_chars_by_step.append(len(strings_list[idx_element]) - len(strings_list[idx_element + 1]))
        # Learn a vocabulary dictionary of all tokens in the raw documents.
        # Transform documents to document-term matrix.
        strings_matrix = co_vec.fit_transform(string_to_compare)
        # Transform the matrix in array
        strings_matrix = strings_matrix.toarray()
        # Calculate the cosine similarity between each vector in the list
        c_sim = cosine_similarity(strings_matrix)
        # Calculate the difference between the value first explanation and the second
        n_line = strings_list[idx_element + 1].count('\n')
        change_by_step.append((c_sim[0][0] - c_sim[0][1]))

    return sum(change_by_step) / len(strings_list), change_by_step, deleted_chars_by_step


def plot_graphs(feature_01_list, feature_02_list, figure_name, heuristic_list):
    """
    The fuction print and save two graphs with feature 01 and feature 02, the x axis is the step number
    :param feature_01_list: list of list of feature
    :param feature_02_list: list of list of feature
    :param figure_name: Name used to save the figure
    """

    fig, ax = plt.subplots(2, 1)
    # plot the chars for each heuristics
    for idx, feature in enumerate(feature_01_list):
        ax[0].plot(np.arange(0, len(feature), 1), feature, label=heuristic_list[idx])
    # plot the step for each heuristics
    for idx, feature in enumerate(feature_02_list):
        ax[1].plot(np.arange(0, len(feature), 1), feature, label=heuristic_list[idx])

    ax[0].set(xlabel='steps',
              ylabel='chars deleted',
              title='Deleted chars per step')
    ax[0].legend()

    ax[1].set(xlabel='steps',
              ylabel='difficulty of the step',
              title='Step understandability')
    ax[1].legend()

    fig.savefig("figure_sub_" + figure_name + ".png")
    plt.show()
