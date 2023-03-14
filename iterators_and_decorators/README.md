# OOP homework  

#### The scripts do not require installation of additional packages:  


## Description  

**Homework for practising of usage classes and OOP**  
Tasks in the nutshell:  

* Write a *MyDict* class that will completely replicate the behavior of a regular dictionary, except that it return both keys and values while iterating.

* Write an *iter_append()* function that "adds" a new element to the end of the iterator, returning an iterator that includes the original elements and the new element  

* Two classes MyString and MySet, which are child classes of str and set, but also carry additional methods. Find and implement a convenient way to make such methods return an instance of the current class, not the parent class  

* Write a *switch_privacy* decorator, which makes all public methods of the class private, all private methods - public. Dunder methods and protected methods remain unchanged.

* Write a context manager *OpenFasta*, that is quite similar to *open()*, but returns *FastRecord* (dataclass) objects with informations about each fasta record (id, description and sequence)

* Write several functions to calculate appearance probability of particular genotype and to show all possible genotypes after crossbreeding of diploid organisms.



## Contents  

1) **scripts** directory - contains scripts in .ipynb and .py format  
2) **data** directory - contains example data for usage of *OpenFasta* context manager and output text files of all possible genotypes from last task.
