import os
import common_functions as common

from os import listdir

if __name__ == "__main__":

    input_ontology = 'datasets/pizza.owl'
    inputSubclassStatements = "datasets/subClasses.nt"
    signature = 'datasets/signature.txt'
    method = '1'
    total_explanations_list = []

    # Save sub_lasses
    sub_classes_list = common.save_subclasses(input_ontology, 3)

    # Get all the justifications file
    exp_files_list = listdir(os.path.abspath(os.getcwd()) + '/datasets/')
    for file in exp_files_list[:]:
        if 'exp' not in file:
            exp_files_list.remove(file)

    # Every sublass
    for idx_class, sub_class in enumerate(sub_classes_list):

        explanations_list = []
        input_ontology = 'datasets/pizza.owl'
        url_classes = []
        url_to_remove = []
        explanation = 'datasets/exp-1.omn'

        sentence_to_prove_file = 'datasets/sentence_to_prove.nt'
        with open(sentence_to_prove_file, 'w') as sentence_to_prove:
            sentence_to_prove.write(sub_class)

        explanations_list.append(
            '-----------------------------------------SENTENCE TO PROVE--------------------------------------------------')
        explanations_list.append(sub_class)
        explanations_list.append('----------------------------------------------------------------------------------------')
        explanations_list.append(
            '-------------------------------------------------DL REASONING-----------------------------------------------')

        # Save the explanation
        common.save_explanations(input_ontology, sentence_to_prove_file)
        # Get the explanation as string
        exp_string = common.get_string_from_file(explanation)
        if exp_string not in explanations_list: explanations_list.append(exp_string)
        # Get the classes and the properties from the ontology
        classes_properties = common.get_classes(input_ontology, False) + common.get_properties(input_ontology, False)

        # For each class in the ontology
        for cla_pro in classes_properties:
            if '<' + cla_pro.iri + '>' not in exp_string and cla_pro.iri not in url_to_remove:
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
            common.save_explanations(input_ontology, sentence_to_prove_file)
            # Get the explanation as string
            exp_string = common.get_string_from_file(explanation)
            if exp_string not in explanations_list: explanations_list.append(exp_string)
            # Get the sentence to prove as a string
            sentence_string = common.get_string_from_file(sentence_to_prove_file)
            # Get classes and properties from the ontology
            classes_properties = common.get_classes(input_ontology, True) + common.get_properties(input_ontology, True)

            # For each class in the ontology
            for cla_pro in classes_properties:
                if '<' + cla_pro.iri + '>' not in sentence_string and cla_pro.iri not in url_to_remove:
                    url_to_remove.append(cla_pro.iri)
                    find = True
                    break

            common.write_signature_to_remove(url_to_remove, signature)
            common.forget_copy_result(input_ontology, method, signature)

        total_explanations_list = total_explanations_list + explanations_list

    try:
        os.remove('result.owl')
        os.remove('datasets/sentence_to_prove.nt')
        os.remove('datasets/signature.txt')
        os.remove('datasets/exp-1.omn')
    except:
        print('Clean phase in error, file not found')

    common.write_result(total_explanations_list)
