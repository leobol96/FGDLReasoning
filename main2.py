import os
import shutil
from os import listdir
import filecmp

import common_functions as common

if __name__ == "__main__":

    input_ontology = 'datasets/pizza.owl'
    signature = 'datasets/signature.txt'
    inputSubclassStatements = "datasets/subClasses.nt"
    method = '3'
    exp_files_list = []
    sub_classes_list = []
    total_explanations_list = []

    # Save sub_lasses
    sub_classes_list = common.save_subclasses(input_ontology, 1)
    # Save the explanation
    common.save_explanations(input_ontology, inputSubclassStatements)
    # Save sentence to prove

    # Get all the justifications file
    exp_files_list = listdir(os.path.abspath(os.getcwd()) + '/datasets/')
    for file in exp_files_list[:]:
        if 'exp' not in file:
            exp_files_list.remove(file)

    # Every sublass
    for idx_class, sub_class in enumerate(sub_classes_list):

        url_in_explanation = []
        explanations_list = []

        # Get the explanation as string
        exp_string = common.get_string_from_file('datasets/exp-' + str(idx_class + 1) + '.omn')
        if exp_string not in explanations_list: explanations_list.append(exp_string)

        signature_file_name = 'datasets/signature_file.nt'
        with open(signature_file_name, 'w') as signature_file:
            signature_file.write(sub_class)

        elements = common.get_element(exp_string)

        for element in elements:
            if '<' + element + '>' not in sub_class and element in exp_string:
                tmp = [element]
                common.write_signature_to_remove(tmp, signature)
                common.forget_copy_result('datasets/exp-' + str(idx_class + 1) + '.omn', method, signature)
                shutil.copy(os.path.abspath(os.getcwd()) + '/result.owl',
                            os.path.abspath(os.getcwd()) + '/datasets/exp-' + str(idx_class + 1) + '.omn')

                common.save_explanations('datasets/exp-' + str(idx_class + 1) + '.omn', signature_file_name)

                explanations_list.append('########FORGETTING########')
                explanations_list.append(element)
                explanations_list.append('##########################')

                # Get the explanation as string
                exp_string = common.get_string_from_file('datasets/exp-' + str(idx_class + 1) + '.omn')
                if exp_string not in explanations_list and '<?xml' not in exp_string: explanations_list.append(exp_string)

        total_explanations_list = total_explanations_list + explanations_list

    # Print the sentence to prove
    print(
        '---------------------------------------------------TO '
        'PROVE-------------------------------------------------')
    print(common.get_string_from_file(inputSubclassStatements))
    # Print the explanation
    print(
        '-------------------------------------------------DL '
        'REASONING-----------------------------------------------')
    for ex in total_explanations_list:
        print(ex)

    print(
        '------------------------------------------------------END'
        '---------------------------------------------------')
