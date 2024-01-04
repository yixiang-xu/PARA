##### supporting function: check_pitch (detect pitch TPL pattern word by word), e.g. GrEAt

import re 
import pandas as pd 

def check_pitch(wordlist):
    
    if str(type(wordlist))!= "<class 'list'>":
        print("the type of the textline should be list")
        return

    ## keep only words that are partially capitalized (but not just only first or end letter):
    wordlist_temp = []
    for w in wordlist:
        word_cap_count = 0
        for l in w:
            if l.isupper():
                word_cap_count = word_cap_count + 1 
        if len(w)>word_cap_count and word_cap_count!=0 and word_cap_count!=1:
            wordlist_temp = wordlist_temp + [w]
        elif word_cap_count ==1:
            if not w[0].isupper() and not w[-1].isupper():
                wordlist_temp = wordlist_temp + [w]

    wordlist = wordlist_temp
    

    ## delete the words that are (repeated) single alphabet letters
    wordlist = [w for w in wordlist if len(set(w))!=1]

    return wordlist






