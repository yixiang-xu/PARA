##### Detect_Spelling (Detection of words whose letters are connected by the same symbol e.g. s-l-o-w)

import re
import pandas as pd 
def Detect_Spelling(textline,word_list,brown_dic,acron_list):

    if str(type(textline))!= "<class 'str'>":
        print("the type of the textline should be string")
        return

    ######### pre-processing the text #########
    textline = textline.split()
    wordlist = []
    for w in textline:
        if w.startswith("#") or w.startswith("http:") or w.startswith("https:") or w.startswith("@") or w.startswith("RT"):
            wordlist = wordlist + ["tplandrea"]
        else:
            wordlist = wordlist + [w]

    textline = " ".join(wordlist) + "\n"

    word_list = [w.lower() for w in word_list]
    acron_list = [w.lower() for w in acron_list]

    #eng_dic = enchant.Dict("en_US")
    rep_count = 0

    ######### find spelling pattern #########
    # find patterns using regular expression alphebat + symbol:
    
    # Letter(symbol)Letter(symbol)Letter(symbol)
    r1 = re.compile(r'(([a-zA-Z])([\*])){2,}(([a-zA-Z])([\*]?))')
    r2 = re.compile(r'(([a-zA-Z])([\.])){2,}(([a-zA-Z])([\.]?))')
    r3 = re.compile(r'(([a-zA-Z])([\-])){2,}(([a-zA-Z])([\-]?))')
    r4 = re.compile(r'(([a-zA-Z])([\!])){2,}(([a-zA-Z])([\!]?))')
    r5 = re.compile(r'(([a-zA-Z])([\~])){2,}(([a-zA-Z])([\~]?))')
    r5 = re.compile(r'(([a-zA-Z])([ ])){2,}(([a-zA-Z])([^a-zA-Z]))')

    r_list = [r1,r2,r3,r4,r5]
    #new_wordlist = wordlist
    for r in r_list:
        rep_pattern = [w.group() for w in r.finditer(textline)]
        if len(rep_pattern)!=0:
            for item in rep_pattern:
                word_ns = "".join([l for l in item if l.isalpha()])
                if word_ns.lower() not in acron_list:
                    if word_ns in brown_dic or word_ns.lower() in word_list or word_ns.lower() in brown_dic:
                        rep_count = rep_count + 1



 
    return rep_count



