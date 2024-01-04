##### Detect_Emphasis (Detection of word/phrase repetition as well as exclamation and/or question mark repetition at sentencen level, the emphasis detector within word is contained in Detect_Wordbased_TPL > check_emphasis)

import re
def Detect_Emphasis(textline):

    if str(type(textline))!= "<class 'str'>":
        print("the type of the textline should be string")
        return

    ######### pre-processing the text #########
    textline = textline.split()
    wordlist = []
    for w in textline:
        if ("#" in w) or ("http:" in w) or ("https:" in w) or ("@" in w) or ("RT" in w):
            wordlist = wordlist + ["tplandrea"]
        else:
            wordlist = wordlist + [w]

    textline = " ".join(wordlist) + "\n"
    # first, change the text to a list of words
    wordlist = re.split(' ',textline)

    rep_intst_vq = 0
    rep_vq = 0
    
    ######### checking the emphasis pattern #########
    
    # the pattern under search is word{space}word{space}word{space}, in which the {space} in the third/last unit can be optional
    # first we search for two units of the pattern, then we search for the third unit
    r = re.compile(r"([^0-9]+? )\1+") # ? allows for non-greedy search, check for any two repetitions (the reason for not setting three repetitions directly is to allow no space for the third repetition)
    w_rep = r.findall(textline)
    if len(w_rep)!=0:
        # check if there is a third repetition
        for w in list(set(w_rep)):
            w_hat = ""
            for i in w: # if w contains symbol, \\ has to be added in front of the symbol for regular expression
                if len(re.findall(r"[0-9A-Za-z ]",i))!=0:
                    w_hat = w_hat + i
                else:
                    w_hat = w_hat + "\\"+ i
            if len(w_hat.split())==1:# for word emphasis e.g. wowowow has to be one unit to count as word
                if len(re.findall(r"[a-zA-Z]",w_hat))>1 and ('tplandrea' not in w): # for word emphasis, one single letter can not be the unit
                    w_ns = w_hat.split()[0]
                    #string = r'('+w_hat+w_hat+w_ns+')'
                    string = r'('+w_hat+')\\1+'+w_ns
                    w_rep_3 = re.finditer(string, textline)
                    w_rep_3 = [w.group() for w in w_rep_3]
                    if len(w_rep_3)>0:
                        intst_vq = [len(re.findall(w_ns,w))/3 for w in w_rep_3]
                        count_vq = [1 for w in w_rep_3]
                        #rep_vq = rep_vq + len(w_rep_3)
                        rep_intst_vq =  rep_intst_vq + sum(intst_vq)
                        rep_vq = rep_vq + sum(count_vq)
            else:
                if 'tplandrea' not in w: # for phrase emphasis, okay single letters be the unit
                    w_ns = w_hat.split()[0]
                    #string = r'('+w_hat+w_hat+w_ns+')'
                    string = r'('+w_hat+')\\1+'+w_ns
                    w_rep_3 = re.finditer(string, textline)
                    w_rep_3 = [w.group() for w in w_rep_3]
                    if len(w_rep_3)>0:
                        intst_vq = [len(re.findall(w_ns,w))/3 for w in w_rep_3]
                        count_vq = [1 for w in w_rep_3]
                        #rep_vq = rep_vq + len(w_rep_3)
                        rep_intst_vq =  rep_intst_vq + sum(intst_vq)
                        rep_vq = rep_vq + sum(count_vq)


    # exclamation/QM point empahsis is conducted here:

    vq_sb = re.compile(r"([\?\!]){2,}\1*")
    vq_sb_rep = [w.group() for w in vq_sb.finditer(textline)]
    # if more than two ! or ? or !? appear, it counts as emphasis for sure
    vq_intst_sb_rep = [max(1,len(w)/3) for w in vq_sb_rep]
    vq_sb_rep = [1 for w in vq_sb_rep]
    rep_intst_vq =  rep_intst_vq + sum(vq_intst_sb_rep)
    rep_vq = rep_vq + sum(vq_sb_rep)

    vq_sb = re.compile(r"([\?\!] ){1,}\1*[\?\!]")
    vq_sb_rep = [w.group() for w in vq_sb.finditer(textline)]
    vq_sb_rep = ["".join(w.split()) for w in vq_sb_rep]
    vq_intst_sb_rep = [max(1,len(w)/3) for w in vq_sb_rep]
    vq_sb_rep = [1 for w in vq_sb_rep]
    rep_intst_vq =  rep_intst_vq + sum(vq_intst_sb_rep)
    rep_vq = rep_vq + sum(vq_sb_rep)


    return rep_vq,rep_intst_vq

