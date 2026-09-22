import numpy as np
import matplotlib.pyplot as plt
#Bisection method for finding a local max

# Derivative F'(x) = -2x + 4
def df(x):
    return -2 * x + 4

#Bracket [a, b] containing root
a, b = 0.0, 3.0
tolerance = 1e-5

#looping each bisection
"""for step in range(20):
    c = (a + b) / 2.0                       #c is our midpoint and we want to make it become the maxima
    if df(c) == 0 or (b - a) < tolerance:   
        break
    if df(c) * df(a) < 0:
        b = c
    else:
        a = c"""
for i in range(100): 
    c = (a+b) /2 