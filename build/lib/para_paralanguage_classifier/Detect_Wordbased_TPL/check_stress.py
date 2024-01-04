##### supporting function: check_stress (detect stress TPL pattern word by word), e.g. GREAT

import re 
import sys
import pandas as pd

def check_stress(wordlist,acron_list):

    if str(type(wordlist))!= "<class 'list'>":
        print("the type of the textline should be list")
        return


    ## keep only words that are capitalized:
    wordlist = [w for w in wordlist if w.isupper()]

    ## delete the words that are (repeated) single alphabet letters
    wordlist = [w for w in wordlist if len(set(w))!=1]

    ## delete the words that are in acron_list
    wordlist = [w for w in wordlist if w not in acron_list]
    


    return wordlist




