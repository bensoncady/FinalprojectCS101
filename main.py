from builddata import *
import pandas as pd



def high_value(energy):
    ill = 0
    for x in energy:
        if x.housing > ill:
            ill = x.housing
    print(ill)

