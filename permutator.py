"""
    Permutator class
"""
import sys
import os
import re
import time # .sleep(), .time(), .time_ns()
import numpy as np

class Permutator:

    def __init__():
        pass
def ceasar(text):
    """
        Modular
    """
    for alpha in ALPHAS:
        print("\n\n----- NEW ALPHA : " + alpha + " -----")
        for inc in range(0, len(alpha)):
            print("inc = " + str(inc))
            new = []
            for i in range(0, len(text)):
                new.append(alpha[(alpha.index(text[i])+inc) % len(alpha)])
            print(''.join(new))