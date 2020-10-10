import os
import common_functions as common

from os import listdir

if __name__ == "__main__":

    input_ontology = 'datasets/pizza.owl'
    inputSubclassStatements = "datasets/subClasses.nt"
    signature = 'datasets/signature.txt'
    method = '1'
    total_explanations_list = []
    heuristic = 'random'

    # Save sub_classes in subClasses.nt
    # sub_classes_list = common.save_subclasses(input_ontology, 1)
    sub_classes_list = common.read_sublasses()

    # Every sublass
    for sub_class in sub_classes_list:

        explanations_list_similarity = []
        explanations_list = []
        input_ontology = 'datasets/pizza.owl'
        url_to_remove = []
        explanation = 'datasets/exp-1.omn'

        # Save the sentence we want to proof in a file
        sentence_to_prove_file = 'datasets/sentence_to_prove.nt'
        with open(sentence_to_prove_file, 'w') as sentence_to_prove:
            sentence_to_prove.write(sub_class)

        # Add sentence to proof to the full explanation
        explanations_list.append('-----------------------------------------SENTENCE TO PROVE--------------------------------------------------')
        explanations_list.append(sub_class)
        explanations_list.append('-------------------------------------------------DL REASONING-----------------------------------------------')


        # Get the explanation from ontologt and save it in exp-#.omn
        common.save_explanations(input_ontology, sentence_to_prove_file)

        # Get the explanation as string
        exp_string = common.get_string_from_file(explanation)

        if exp_string not in explanations_list:
            explanations_list.append('-------------------------------------------------REMOVE BULK-----------------------------------------------')
            explanations_list.append(exp_string)
            explanations_list_similarity.append(exp_string)

        # Get the classes and the properties from the ontology
        classes = common.get_classes(input_ontology, False)
        props = common.get_properties(input_ontology, False)
        classes_properties = classes + props

        # Filter out all of the items that are not in the explanation
        for cla_pro in classes_properties:
            if '<' + cla_pro.iri + '>' not in exp_string and cla_pro.iri not in url_to_remove:
                url_to_remove.append(cla_pro.iri)

        # Remove all of the filtered items
        common.write_signature_to_remove(url_to_remove, signature)
        common.forget_copy_result(input_ontology, method, signature)
        # THIS CHANGES THE ONTOLOGY, WHEN RECALCULATING CLASSES IT CREATES NANS
        # THE FORGET FUNCTION FORGETS TOO MUCH OR ERRORS

        # Iteratively remove items until proof has been reached
        find = True
        input_ontology = 'datasets/result.owl'

        while find:
            find = False
            url_to_remove = []

            # Get the explanation for the new ontology and save in exp-#.omn
            common.save_explanations(input_ontology, sentence_to_prove_file)

            # Get the explanation as string
            exp_string = common.get_string_from_file(explanation)

            # Stop if the explanation contains 'Nothing'
            if 'Nothing' in exp_string:
                print('SYSTEM ERROR')
                break

            # Add explanation to final explanation
            explanations_list.append('-------------------------------------------------NEW EXPLANATION-----------------------------------------------')
            explanations_list.append(exp_string)
            explanations_list_similarity.append(exp_string)

            # Get the sentence to prove as a string
            sentence_string = common.get_string_from_file(sentence_to_prove_file)

            heuristic = 'max'
            # select the class to remove
            signature_to_forget = common.select_signature(input_ontology, exp_string, sentence_string, heuristic)
            if signature_to_forget:
                url_to_remove.append(signature_to_forget)
                find = True
                explanations_list.append('\n########### FORGETTING ##############')
                explanations_list.append(signature_to_forget + '\n')

                # Write the signature to the signature file
                common.write_signature_to_remove(url_to_remove, signature)

                # Forget the signature
                common.forget_copy_result(input_ontology, method, signature)

        print("The value of the similarity is:" + str(common.get_list_similarity(explanations_list_similarity)))

        total_explanations_list = total_explanations_list + explanations_list

    try:
        os.remove('result.owl')
        os.remove('datasets/result.owl')
        os.remove('datasets/sentence_to_prove.nt')
        os.remove('datasets/signature.txt')
        os.remove('datasets/exp-1.omn')
    except:
        print('Clean phase in error, file not found')

    common.write_result(total_explanations_list)
