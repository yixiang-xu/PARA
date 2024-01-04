##### main function: Detect_Asterisk_TPL (detection of TPL elements that are characterized by the asterisk pattern, including VQ volume, VS differentiators, TK alphahaptics, VK alphakinesics, Artifact emoji symbol)
from .check_asterisk import check_asterisk
import re
import pandas as pd
def Detect_Asterisk_TPL(textline, keyword_dic):
     
    if str(type(textline))!= "<class 'str'>":
        print("the type of the textline should be string")
        return

    if str(type(keyword_dic))!= "<class 'dict'>":
        print("the type of the key_word_dic should be dictionary")
        return

    ######### pre-processed the input text #############
    textline = textline.split()
    wordlist = []
    for w in textline:
        if w.startswith("#") or w.startswith("https:") or w.startswith("http:") or w.startswith("@") or w.startswith("RT"):
            wordlist = wordlist + ["tplandrea"]
        else:
            wordlist = wordlist + [w]

    textline = " ".join(wordlist) + "\n"

    ######### detecting the asterisk pattern #############
    vq_count = 0
    vs_count = 0
    tk_count = 0
    vk_count = 0
    a_count = 0
    
    
    vq_count = check_asterisk(textline, keyword_dic, type="vq")
    tk_count = check_asterisk(textline, keyword_dic, type="tk")
    vk_count = check_asterisk(textline, keyword_dic, type="vk")
    vs_count = check_asterisk(textline, keyword_dic, type="vs")
    a_count = check_asterisk(textline, keyword_dic, type = "a")

    return vq_count, vs_count, tk_count, vk_count, a_count


