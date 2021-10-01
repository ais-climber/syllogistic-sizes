# models.py
# 
# Author: Caleb Kisby
# Date of conception: 15 Aug 2018
# Date last modified: 16 Aug 2018
# 
# Class to represent and manipulate models of nouns, where the nouns
# are interpreted as sets.
# 
# We also include boolean functions used to evaluate the truth of the
# following types of sentences (in a specified model):
# 
# 'all a are b'
# 'some a are b'
# 'no a are b'
# 'there are at least as many a as b'
# 'thre are more a than b'
# 
# The semantics of these sentences, and the specification of the logic
# involving these sentences, is detailed in Larry Moss' paper
# _Syllogistic Logic With Cardinality Comparisons_
# https://www.researchgate.net/publication/314889069_Syllogistic_Logic_with_Cardinality_Comparisons
# 

symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class Model():
    def __init__(self, num_nouns):
        self.num_nouns = num_nouns
        self.nouns = symbols[0 : num_nouns]
        self.sets = {noun : set() for noun in self.nouns}

    # Adds the 'element' to the 'noun'.  
    def add(self, noun, element):
        self.sets[noun].add(element)

    def remove(self, noun, element):
        self.sets[noun].remove(element)
        
    # A boolean function that returns whether this model
    # already contains the 'element' in the given 'noun'.
    def contains(self, noun, element):
        return element in self.sets[noun]
    
    # Returns the size of the universe of the model, i.e. the number of
    # distinct elements in the model.
    # TODO: Does not work yet
    def size(self):
        total_elements = set().union(self.sets[noun] for noun in self.nouns)
        return len(total_elements)

    # Returns the total number of items listed in the model.
    # TODO: Does not work yet
    def order(self):
        total_items = []
        for noun in self.nouns:
            total_items = total_items + list(self.sets[noun])
    
        return len(total_items)
    
    # Returns a copy of this model.
    # (This might be needed (?) because the sets within the model are mutable?)
    def copy(self):
        model_copy = Model(self.num_nouns)
        
        for noun in self.nouns:
            for element in self.sets[noun]:
                model_copy.add(noun, element)
                
        return model_copy

    def __hash__(self):
        return hash((hash(tuple(nounset)) for nounset in self.sets))
    
    def __eq__(self, modelB):
        # If the two models differ in number of nouns, then the
        # two are incomparable by convention.
        if self.nouns != modelB.nouns:
            return False
        
        # Ensure that both models contain the same noun sets.
        for noun in self.nouns:
            if self.sets[noun] != modelB.sets[noun]:
                return False
        
        return True
    
    # We overload the '<=' operator for models.
    # modelA <= modelB iff modelA is a sub-model of modelB.
    def __le__(self, modelB):
        # If the two models differ in number of nouns, then the
        # two are incomparable by convention.
        if self.nouns != modelB.nouns:
            return False
        
        # If one noun is not a subset of the other, return False.
        for noun in self.nouns:
            if not self.sets[noun].issubset(modelB.sets[noun]):
                return False
        
        return True
    
    # We overload the '<' operator for models.
    # modelA < modelB iff modelA is a *STRICT* sub-model of modelB.
    # same as the '<=' overload, except modelA and modelB must be distinct.
    def __lt__(self, modelB):
        # If the two models differ in number of nouns, then the
        # two are incomparable by convention.
        if self.nouns != modelB.nouns:
            return False
        
        is_distinct = False
        is_subset = True
        
        # If one noun is not a subset of the other, return False.
        for noun in self.nouns:
            if self.sets[noun] != modelB.sets[noun]:
                is_distinct = True
            
            if not self.sets[noun].issubset(modelB.sets[noun]):
                is_subset = False
        
        return is_subset and is_distinct
    
    def __str__(self):
        result = ""

        for noun in self.sets:
            result += noun + ": " + str(self.sets[noun]) + "\n"

        return result

# The semantics of these sentences come straight out of Larry Moss'
# aforementioned paper:
# https://www.researchgate.net/publication/314889069_Syllogistic_Logic_with_Cardinality_Comparisons

def all(model, nounA, nounB):
    return model.sets[nounA].issubset(model.sets[nounB])

def some(model, nounA, nounB):
    return model.sets[nounA].intersection(model.sets[nounB]) != set()

def no(model, nounA, nounB):
    return model.sets[nounA].intersection(model.sets[nounB]) == set()

def atLeastAsMany(model, nounA, nounB):
    return len(model.sets[nounA]) >= len(model.sets[nounB])

def moreThan(model, nounA, nounB):
    return len(model.sets[nounA]) > len(model.sets[nounB])

# Function to negate a noun in a model.  Returns a 'set' of all
# elements in the model that are not in the noun.
def neg(model, noun):
    not_noun = {}
    
    for nounset in model:
        if (nounset != noun):
            not_noun = not_noun.union(nounset)
        
    return not_noun

# A wrapper around 'neg' for when we don't know if the noun needs to be negated.
def maybe_neg(model, noun, negate=False):
    if negate:
        return neg(model, noun)
    else:
        return noun

# Function for generating all possible models with a specified
# number of nouns, maximum number of elements, and maximum 'bound' order.
def generate_recursive(model, num_nouns, num_elements, bound):
    if (model.order() == bound):
        return [model]
    elif (model.order() < bound):
        generated_models = [model]
        
        for noun in model.nouns:
            for element in range(0, num_elements):
                
                # We have to make sure we do not add an existing element into the
                # model again, since this would cause infinite recursion.
                if not model.contains(noun, element):
                    model.add(noun, element)
                    generated_models = generated_models + [model]
                    
                    # Note that we obtain a copy of this model, because stupid Python sets are stupidly mutable...
                    generated_models = generated_models + generate_recursive(model.copy(), num_nouns,
                                                                             num_elements, bound)
                    model.remove(noun, element)
        
        return generated_models
    else:
        print("The base model is larger than the bound!")
