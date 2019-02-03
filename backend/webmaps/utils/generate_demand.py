""" Utility module to generate demand. """
import random as rand 

def generate_demand():
    """ Retrun a list of demands per hour """
    rand_demands = list()
    for i in range(24):
        rand_demands.append(round(rand.random(), 2))
    
    return rand_demands