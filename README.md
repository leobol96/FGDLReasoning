# Forgetting Reasoning on Pizza Ontology

The project is built for using the Forgetting reasoning on the Pizza ontology. 
Please read carefully this README file before using the program. If you don't have a markdown editor or if you don't see the images, please visit: https://github.com/leobol96/FGDLReasoning

## Structure

The project is made up of three main files.
- *main.py*: The main file contains the principal algorithm to simplify the ontology using the forgetting paradigm
- *heuristic_function.py* The heuristic file contains the functions used to select the correct element to delete during the forgetting method
- *common_function.py* The common contains all the general functions used to read, write, plot etc.

## How to run the project

The Reasoner is static and always analyzes the same subclasses relationship. This because sometimes the lethe.jar and the kr_functions.jar crash for unknown reasons.
So, to run the code simply from command line:

python main.py

## Dependencies

The main program uses the following dependencies:
- os
- shutil
- matplotlib.pyplot 
- numpy
- owlready2 
- sklearn
- re
- random 
So to run the code, please be sure to have all the dependencies installed on the pc.

## At the end of the execution

After running the main.py the following plot will be printed :

![structure](https://github.com/leobol96/FGDLReasoning/blob/master/img/FourSeasons_DomainConcept.png)
![structure](https://github.com/leobol96/FGDLReasoning/blob/master/img/Siciliana_DomainConcept.png)
![structure](https://github.com/leobol96/FGDLReasoning/blob/master/img/Soho_Food.png)
![structure](https://github.com/leobol96/FGDLReasoning/blob/master/img/Veneziana_VegetarianPizzaEquivalent1.png)

Moreover, you will be able to find all the justifications in the file FG_EXPLANATIONS.txt
The follow is an example of justifications during the forgetting reasoning:

########### SIMILARITY ##############
-----------------------------------------SENTENCE TO PROVE--------------------------------------------------
<http://www.co-ode.org/ontologies/pizza/pizza.owl#Siciliana> rdfs:subClassOf <http://www.co-ode.org/ontologies/pizza/pizza.owl#DomainConcept> .
-------------------------------------------------DL REASONING-----------------------------------------------
-------------------------------------------------REMOVE BULK-----------------------------------------------
Ontology(<http://www.example.com/explanation1>
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#Siciliana> <http://www.co-ode.org/ontologies/pizza/pizza.owl#NamedPizza>)
SubObjectPropertyOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#isBaseOf> <http://www.co-ode.org/ontologies/pizza/pizza.owl#isIngredientOf>)
InverseObjectProperties(<http://www.co-ode.org/ontologies/pizza/pizza.owl#hasIngredient> <http://www.co-ode.org/ontologies/pizza/pizza.owl#isIngredientOf>)
ObjectPropertyDomain(<http://www.co-ode.org/ontologies/pizza/pizza.owl#hasIngredient> <http://www.co-ode.org/ontologies/pizza/pizza.owl#Food>)
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#NamedPizza> <http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza>)
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#Food> <http://www.co-ode.org/ontologies/pizza/pizza.owl#DomainConcept>)
InverseObjectProperties(<http://www.co-ode.org/ontologies/pizza/pizza.owl#hasBase> <http://www.co-ode.org/ontologies/pizza/pizza.owl#isBaseOf>)
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza> ObjectSomeValuesFrom(<http://www.co-ode.org/ontologies/pizza/pizza.owl#hasBase> <http://www.co-ode.org/ontologies/pizza/pizza.owl#PizzaBase>))
)
-------------------------------------------------NEW EXPLANATION-----------------------------------------------
Ontology(<http://www.example.com/explanation1>
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#Siciliana> <http://www.co-ode.org/ontologies/pizza/pizza.owl#NamedPizza>)
SubObjectPropertyOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#hasBase> <http://www.co-ode.org/ontologies/pizza/pizza.owl#hasIngredient>)
SubClassOf(ObjectSomeValuesFrom(<http://www.co-ode.org/ontologies/pizza/pizza.owl#hasIngredient> owl:Thing) <http://www.co-ode.org/ontologies/pizza/pizza.owl#Food>)
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#NamedPizza> <http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza>)
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#Food> <http://www.co-ode.org/ontologies/pizza/pizza.owl#DomainConcept>)
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza> ObjectSomeValuesFrom(<http://www.co-ode.org/ontologies/pizza/pizza.owl#hasBase> <http://www.co-ode.org/ontologies/pizza/pizza.owl#PizzaBase>))
)

########### FORGETTING ##############
http://www.co-ode.org/ontologies/pizza/pizza.owl#NamedPizza

-------------------------------------------------NEW EXPLANATION-----------------------------------------------
Ontology(<http://www.example.com/explanation1>
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#Siciliana> <http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza>)
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza> <http://www.co-ode.org/ontologies/pizza/pizza.owl#Food>)
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#Food> <http://www.co-ode.org/ontologies/pizza/pizza.owl#DomainConcept>)
)

########### FORGETTING ##############
http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza

-------------------------------------------------NEW EXPLANATION-----------------------------------------------
Ontology(<http://www.example.com/explanation1>
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#Siciliana> ObjectSomeValuesFrom(<http://www.co-ode.org/ontologies/pizza/pizza.owl#hasBase> <http://www.co-ode.org/ontologies/pizza/pizza.owl#PizzaBase>))
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#Food> <http://www.co-ode.org/ontologies/pizza/pizza.owl#DomainConcept>)
SubClassOf(ObjectSomeValuesFrom(<http://www.co-ode.org/ontologies/pizza/pizza.owl#hasBase> owl:Thing) <http://www.co-ode.org/ontologies/pizza/pizza.owl#Food>)
)

########### FORGETTING ##############
http://www.co-ode.org/ontologies/pizza/pizza.owl#hasBase

-------------------------------------------------NEW EXPLANATION-----------------------------------------------
Ontology(<http://www.example.com/explanation1>
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#Food> <http://www.co-ode.org/ontologies/pizza/pizza.owl#DomainConcept>)
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#Siciliana> <http://www.co-ode.org/ontologies/pizza/pizza.owl#Food>)
)

########### FORGETTING ##############
http://www.co-ode.org/ontologies/pizza/pizza.owl#Food

-------------------------------------------------NEW EXPLANATION-----------------------------------------------
Ontology(<http://www.example.com/explanation1>
SubClassOf(<http://www.co-ode.org/ontologies/pizza/pizza.owl#Siciliana> <http://www.co-ode.org/ontologies/pizza/pizza.owl#DomainConcept>)
)
