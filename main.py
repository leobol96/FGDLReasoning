import os
import common_functions as common
import heuristic_functions as hf

if __name__ == "__main__":

    input_ontology = 'datasets/pizza.owl'
    inputSubclassStatements = "datasets/subClasses.nt"
    signature_file_dir = 'datasets/signature.txt'
    method = '1'
    total_explanations_list = []
    heuristic = 'combined_max'
    error_file = "datasets/error.txt"

    # Save sub_classes in subClasses.nt
    #sub_classes_list = common.save_subclasses(input_ontology, 1)
    sub_classes_list = common.read_sublasses()

    for sub_class in sub_classes_list:
        explanation_dir = 'datasets/exp-1.omn'
        explanations_list_similarity = []
        explanations_list = []
        url_to_remove = []

        average_similarity = 0
        deleted_chars_by_step = []
        change_by_step = []
        deleted_chars_by_step_list = []
        change_by_step_list = []


        if common.check_error_proof(sub_class, error_file):
            print('This one not good')
            continue

        # Save the sentence we want to prove in a file
        sentence_to_prove_file = 'datasets/sentence_to_prove.nt'
        with open(sentence_to_prove_file, 'w') as sentence_to_prove:
            sentence_to_prove.write(sub_class)

        # Add sentence to proof to the full explanation
        explanations_list.append(
            '-----------------------------------------SENTENCE TO PROVE--------------------------------------------------')
        explanations_list.append(sub_class)
        explanations_list.append(
            '-------------------------------------------------DL REASONING-----------------------------------------------')

        # Get the explanation from ontology and save it in exp-#.omn
        common.save_explanations(input_ontology, sentence_to_prove_file)

        # Get the explanation as string
        exp_string = common.get_string_from_file(explanation_dir)

        explanations_list.append(
            '-------------------------------------------------REMOVE BULK-----------------------------------------------')
        explanations_list.append(exp_string)
        explanations_list_similarity.append(exp_string)

        # Get the classes and the properties from the ontology
        classes_properties = common.get_classes_properties(input_ontology, False)

        # Filter out all of the items that are not in the explanation
        for cla_pro in classes_properties:
            if '<' + cla_pro.iri + '>' not in exp_string and cla_pro.iri not in url_to_remove:
                url_to_remove.append(cla_pro.iri)

        # Remove all of the filtered items
        common.write_signature_to_remove(url_to_remove, signature_file_dir)
        common.forget_copy_result(input_ontology, '1', signature_file_dir)
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
            exp_string = common.get_string_from_file(explanation_dir)

            # Stop if the explanation contains 'Nothing'
            if 'Nothing' in exp_string:
                print(' -------------- SYSTEM ERROR --------------')
                print(sub_class)
                with open(error_file, 'a') as file:
                    file.write(sub_class)
                break

            # Add explanation to final explanation
            explanations_list.append(
                '-------------------------------------------------NEW EXPLANATION-----------------------------------------------')
            explanations_list.append(exp_string)
            explanations_list_similarity.append(exp_string)

            # select the class to remove
            signature_to_forget = hf.select_signature(sentence_to_prove_file, explanation_dir, input_ontology,
                                                      heuristic)
            if signature_to_forget:
                find = True
                url_to_remove.append(signature_to_forget)
                explanations_list.append('\n########### FORGETTING ##############')
                explanations_list.append(signature_to_forget + '\n')

                # Write the signature to the signature file
                common.write_signature_to_remove(url_to_remove, signature_file_dir)

                # Forget the signature
                common.forget_copy_result(input_ontology, '3', signature_file_dir)

        explanations_list.append('\n########### SIMILARITY ##############')

        average_similarity, change_by_step, deleted_chars_by_step = common.get_list_similarity(explanations_list_similarity)
        change_by_step_list.append(change_by_step)
        deleted_chars_by_step_list.append(deleted_chars_by_step)

        common.plot_graphs(deleted_chars_by_step_list, change_by_step_list, 'plot')
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
