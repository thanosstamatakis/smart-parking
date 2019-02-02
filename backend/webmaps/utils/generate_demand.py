""" Utility module to generate demand. """
import random as rand 

def generate_demand():
    """ Retrun a list of demands per hour """
    rand_demands = list()
    for i in range(23):
        rand_demands.append(round(rand.random()))
    
    return rand_demands