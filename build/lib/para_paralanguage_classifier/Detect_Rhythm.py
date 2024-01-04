##### Detect_Rhythm (Detection of word-symbol alternations e.g. Best. Food. Ever)

import re

import pandas as pd

def Detect_Rhythm(textline, word_list, brown_dic):

    if str(type(textline))!= "<class 'str'>":
        print("the type of the textline should be string")
        return
    
    ######### pre-processing the text #########
    textline = textline.split()
    wordlist = []
    for w in textline:
        if w.startswith("#") or w.startswith("https:") or w.startswith("http:") or w.startswith("@") or w.startswith("RT"):
            wordlist = wordlist + ["tplandrea"]
        else:
            wordlist = wordlist + [w]

    textline = " ".join(wordlist) + "\n"

    word_list = [w.lower() for w in word_list]


    rep_count = 0

    ######### detecting rhythm pattern in the text #########
    
    # allow I'll or I or A to be in the pattern, however when examining it, line 56 which checks len([w for w in word_ns if len(w)>1] would rule them out 
    # i.e., single letters are not counted 
    
    # find pattern using regular expression within word 
    # pattern - Word(symbol)Word(symbol)Word(symbol) here word check against brown_dic, e.g., oh.my.god.,
    r1 = re.compile(r'(([a-zA-Z\']{1,})([\*])){3,}')
    r2 = re.compile(r'(([a-zA-Z\']{1,})([\.])){3,}')
    r3 = re.compile(r'(([a-zA-Z\']{1,})([\-])){3,}')
    r4 = re.compile(r'(([a-zA-Z\']{1,})([\!])){3,}')
    r5 = re.compile(r'(([a-zA-Z\']{1,})([\~])){3,}')

    r_list = [r1,r2,r3,r4,r5]


    for r in r_list:
        rep_pattern = [w.group() for w in r.finditer(textline)]
        if len(rep_pattern)!=0:
            for item in rep_pattern:
                w_count = 0
                word_ns = re.split(r"[\*\.\-\!\~\']", item)
                word_ns = [w for w in word_ns if w !="" and w!=" "]
                for w in word_ns:
                    # eng_dic take I'll, you'll, he'll as english word
                    if w in brown_dic or w.lower() in word_list or w.lower() in brown_dic:
                        w_count = w_count + 1
        # only when the true check matches the # of words we counts
                if w_count >= 3 and len([w for w in word_ns if len(w)>1])>=3:
                    rep_count = rep_count + 1
    
  

    # find pattern using regular expression at sentence level
    # pattern1 - Word(symbol){space}Word(symbol){space}Word(symbol){space} e.g., I. guess. I’ll. go.
    r1 = re.compile(r'(([a-zA-Z\']{1,})([\*])([\s])){2,}(([a-zA-Z\']{1,})([\*])([\s]*))')
    r2 = re.compile(r'(([a-zA-Z\']{1,})([\.])([\s])){2,}(([a-zA-Z\']{1,})([\.])([\s]*))')
    r3 = re.compile(r'(([a-zA-Z\']{1,})([\-])([\s])){2,}(([a-zA-Z\']{1,})([\-])([\s]*))')
    r4 = re.compile(r'(([a-zA-Z\']{1,})([\!])([\s])){2,}(([a-zA-Z\']{1,})([\!])([\s]*))')
    r5 = re.compile(r'(([a-zA-Z\']{1,})([\~])([\s])){2,}(([a-zA-Z\']{1,})([\~])([\s]*))')
    r6 = re.compile(r'(([a-zA-Z\']{1,})([\.])([\s])){2,}(([a-zA-Z\']{1,})([\!])([\s]*))')


    r_list = [r1,r2,r3,r4,r5, r6]
    for r in r_list:
        rep_pattern = [w.group() for w in r.finditer(textline)]
        if len(rep_pattern)!=0:
            for item in rep_pattern:
                word_count = 0 # counting if the word in the sentence pattern is english word or wordlist
                word_ns = re.split(r"[\*\.\-\!\~\' ]", item)
                word_ns = [w for w in word_ns if w !="" and w!=" "]
                for w in word_ns:
                    if w in brown_dic or w.lower() in word_list or w.lower() in brown_dic:
                        word_count = word_count + 1
            # only when the true check matches the # of words
            # and only when the word is not all single letters
                if word_count >=3 and len([w for w in word_ns if len(w)>1])>=3:
                    rep_count = rep_count + 1
  
    # find pattern using regular expression at sentence level
    # pattern2 - Word{space}(symbol){space}Word{space}(symbol){space}Word{space}(symbol){space}
    r1 = re.compile(r'(([a-zA-Z\']{1,})([\s])([\*])([\s])){2,}(([a-zA-Z\']{1,})([\s])([\*])([\s]*))')
    r2 = re.compile(r'(([a-zA-Z\']{1,})([\s])([\.])([\s])){2,}(([a-zA-Z\']{1,})([\s])([\.])([\s]*))')
    r3 = re.compile(r'(([a-zA-Z\']{1,})([\s])([\-])([\s])){2,}(([a-zA-Z\']{1,})([\s])([\-])([\s]*))')
    r4 = re.compile(r'(([a-zA-Z\']{1,})([\s])([\!])([\s])){2,}(([a-zA-Z\']{1,})([\s])([\!])([\s]*))')
    r5 = re.compile(r'(([a-zA-Z\']{1,})([\s])([\~])([\s])){2,}(([a-zA-Z\']{1,})([\s])([\~])([\s]*))')
    r6 = re.compile(r'(([a-zA-Z\']{1,})([\s])([\.])([\s])){2,}(([a-zA-Z\']{1,})([\s])([\!])([\s]*))')



    r_list = [r1,r2,r3,r4,r5,r6]
    for r in r_list:
        rep_pattern = [w.group() for w in r.finditer(textline)]
        if len(rep_pattern)!=0:
            for item in rep_pattern:
                word_count = 0 # counting if the word in the sentence pattern is english word or wordlist
                word_ns = re.split(r"[\*\.\-\!\~\' ]", item)
                word_ns = [w for w in word_ns if w !="" and w!=" "]
                for w in word_ns:
                    if w in brown_dic or w.lower() in word_list or w.lower() in brown_dic:
                        word_count = word_count + 1
                # only when the check matches the # of words i.e. every word in the pattern matches
                # and only when the word is not all single letters
                if word_count >=3 and len([w for w in word_ns if len(w)>1])>=3:
                    rep_count = rep_count + 1
 
    return rep_count




