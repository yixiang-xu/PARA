##### supporting function: check_emoticon (detect emoji TPL pattern)
import re 
from .block_emoticon import block_emoticon
def check_emoticon(textline, emoticon_hier,type):
    
    ### pre-processing emoticon list ###
    if type == "tk":
        target_emoticon = emoticon_hier["tk"]
    elif type == "vk":
        target_emoticon = emoticon_hier["vk"]
    elif type == "a":
        target_emoticon = emoticon_hier["a"]


    emoticon_top, emoticon_mid2, emoticon_mid, emoticon_btm = target_emoticon[0], target_emoticon[1], target_emoticon[2], target_emoticon[3]

    ### check match between emoticon and text ###
    # go through the list from top - mid - mid2 - btm, check match between emoticon and text
    # mt -- match 
    # mt -- match
    mt_top = []
    mt_mid = []
    mt_mid2 = []
    mt_btm = []
    
    # match top emoticon
    mt_top = block_emoticon(emoticon_top, textline) # block emoticon returns two - locations of identified emoticons, and counts of emoticons
    mt_span = mt_top[0]
    # create new text by replacing those identified emoticon by "A" symbol to avoid replicating counting by lower emoticon
    for pr in mt_span:
        textline = textline[:pr[0]] + 'A'*(pr[1]-pr[0]) + textline[pr[1]:]

    # match mid emoticon
    mt_mid = block_emoticon(emoticon_mid,textline)
    mt_span = mt_mid[0]
    # create new text by replacing those identified emoticon by "A" symbol to avoid replicating counting by lower emoticon
    for pr in mt_span:
        textline = textline[:pr[0]] + 'A'*(pr[1]-pr[0]) + textline[pr[1]:]


    # match mid2 emoticon
    mt_mid2 = block_emoticon(emoticon_mid2,textline)
    mt_span = mt_mid2[0]
    # create new text by replacing those identified emoticon by "A" symbol to avoid replicating counting by lower emoticon
    for pr in mt_span:
        textline = textline[:pr[0]] + 'A'*(pr[1]-pr[0]) + textline[pr[1]:]

    # match btm emoticon
    mt_btm = block_emoticon(emoticon_btm,textline)


    mt_count = mt_top[1] + mt_mid[1] + mt_mid2[1] + mt_btm[1]
    mt_intst_count = mt_top[2] + mt_mid[2] + mt_mid2[2] + mt_btm[2]

    intst_emoticon = mt_intst_count
    number_emoticon = mt_count

    return [number_emoticon, intst_emoticon]



    # # match x as a tk emoticon
    # # we count any instance with x and space e.g. xx xxxx xxx as one instance of consecutive x instead of three instances of x
    # if type == "tk":
    #     x_emoticon = [w.group() for w in re.finditer(r"([x ]{2,})",textline)]
    #     x_emoticon = [w.replace(" ", "") for w in x_emoticon]
    #     if len(x_emoticon)>0:
    #         intst_emoticon = mt_intst_count + sum([len(w)/3 for w in x_emoticon if len(w)>3 or len(w)==3]) + sum([1 for w in x_emoticon if len(w)<3]) # again when x shows up three or more than three times it gets discounted by 3
    #         number_emoticon = mt_count + sum([1 for w in x_emoticon])
    #     else:
    #         intst_emoticon = mt_intst_count
    #         number_emoticon = mt_count
    # else:
    #     intst_emoticon = mt_intst_count
    #     number_emoticon = mt_count

