##### supporting function: check_emojis (detect emoji TPL pattern)
import regex 
from collections import Counter

import numpy as np
import re
import pandas as pd 
from itertools import groupby

def check_emojis(textline, key_emoji, type):
    
    ### pre-processing emoji list ###
    if type is "tk":
        key_emoji_s = key_emoji["tk"]
    elif type is "vk":
        key_emoji_s = key_emoji["vk"]
    elif type is "a":
        key_emoji_s = key_emoji["a"]


    data = regex.findall(r'\X',textline)
    data_ls = Counter(data)
    data_ls_key = np.array(list(data_ls.keys()))
    emoji_key = np.array(key_emoji_s)

    data_ls_key = data_ls_key[np.isin(data_ls_key,emoji_key)]
    mt_intst_count = np.sum([data_ls[w] for w in data_ls_key])


    data = [w for w in data if w != ' ']
    data_remove = [i[0] for i in groupby(data)]
    data_norep_ls = Counter(data_remove)

    mt_count = np.sum([data_norep_ls[w] for w in data_ls_key])


    return [mt_count,mt_intst_count]



