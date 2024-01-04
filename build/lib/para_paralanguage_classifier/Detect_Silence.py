##### Detect Silence (Detection of the occurence of ..., ~~~, :::, after three consecutive occurences, every additional occurence in the consecutive row would be counted as one third towards intensity score)

import re
import pandas as pd

def Detect_Silence(textline):

    if str(type(textline))!= "<class 'str'>":
        print("the type of the textline should be string")
        return
    
    ######### pre-processing the text #########
    textline = re.sub(r"\n", "",textline)
    textline = re.sub(r"…", "...",textline) 
    textline = textline.lower()
    # first replace ... more for, ... http:, ... https: with http: 
    textline =  re.sub(r"\.\.\.(\s){0,}http:", r" http:", textline)  # to avoid counting ... because of incomplete website link #\s represents whitespace 
    textline =  re.sub(r"\.\.\.(\s){0,}https:", r" https:", textline)   
    textline = re.sub(r"\.\.\.(\s){0,}more for", r" more for", textline)  # to avoid counting ... because of incomplete sentence
    textline = [w for w in textline.split() if ("#" not in w) and ("http:" not in w) and ("https:" not in w) and ("@" not in w) and ("RT" not in w)]
    textline = "".join(textline)

    ######### detecting silence pattern in the text #########
    vq_sb = re.compile(r"(\:){3,}\1*")
    vq_matched = vq_sb.finditer(textline)
    vq_matched = [w.group() for w in vq_matched]
    vq_intst_sb_rep1 = [len(w) for w in vq_matched] #[max(1,len(w)/3) for w in vq_matched]
    vq_sb_rep1 = [1 for w in vq_sb.finditer(textline)]

    vq_sb = re.compile(r"(\~){3,}\1*")
    vq_matched = vq_sb.finditer(textline)
    vq_matched = [w.group() for w in vq_matched]
    vq_intst_sb_rep2 = [len(w) for w in vq_matched] #[max(1,len(w)/3) for w in vq_matched]
    vq_sb_rep2 = [1 for w in vq_sb.finditer(textline)]


    vq_sb = re.compile(r"(\.){2,}\1*")
    vq_sb_rep3 = [w.group() for w in vq_sb.finditer(textline)]
    # however we have several exceptions not to be counted
    if textline.endswith("..") and not textline.endswith("...."):
        vq_sb_rep3 = vq_sb_rep3[:-1]
    elif textline.endswith("..#") and not textline.endswith("....#"):
        vq_sb_rep3 = vq_sb_rep3[:-1]
    elif textline.endswith("..@") and not textline.endswith("....@"):
        vq_sb_rep3 = vq_sb_rep3[:-1]
    vq_intst_sb_rep3 = [len(w) for w in vq_sb_rep3] #[max(1,len(w)/3) for w in vq_sb_rep3]
    vq_sb_rep3 = [1 for w in vq_sb_rep3]


    vq_sb = re.compile(r"(\_){3,}\1*")
    vq_matched = vq_sb.finditer(textline)
    vq_matched = [w.group() for w in vq_matched]
    vq_intst_sb_rep4 = [len(w) for w in vq_matched] #[max(1,len(w)/3) for w in vq_matched]
    vq_sb_rep4 = [1 for w in vq_sb.finditer(textline)]



    return sum(vq_sb_rep1) + sum(vq_sb_rep2) + sum(vq_sb_rep3) + sum(vq_sb_rep4), sum(vq_intst_sb_rep1) + sum(vq_intst_sb_rep2) + sum(vq_intst_sb_rep3) + sum(vq_intst_sb_rep4)

         
       
