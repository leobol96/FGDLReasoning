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
So, to execute the code, type from command line:

**python main.py**

It was not possible to create an executable because the owlready2 library has compatibility problems with Pyinstaller.

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

So to run the code, please be sure to have all the dependencies installed in the pc.

## At the end of the execution

After running the main.py the following plots will be printed and save in the main directory :

<table>
  <tr>
    <td><img src="https://github.com/leobol96/FGDLReasoning/blob/master/img/FourSeasons_DomainConcept.png" ></td>
    <td><img src="https://github.com/leobol96/FGDLReasoning/blob/master/img/Siciliana_DomainConcept.png" ></td>
  </tr>
 </table>
 
 <table>
    <tr>
    <td><img src="https://github.com/leobol96/FGDLReasoning/blob/master/img/Soho_Food.png" ></td>
    <td><img src="https://github.com/leobol96/FGDLReasoning/blob/master/img/Veneziana_VegetarianPizzaEquivalent1.png" ></td>
  </tr>
 </table>

Moreover, you will be able to find all the justifications in the file FG_EXPLANATIONS.txt
The following is an example of justifications during the forgetting reasoning:


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

## Others

As mentioned above, some times the jar files don't work properly, so if you get any errors or the forgetting phase seems blocked, try to run the software another time.
If errors persist, please contact me.




