##### Detect_Censorship (Detection of censorship)
##### we adopted the algorithm i.e. edit distance approach as well as the censorship word list from Wenbo Wang et.al (2014, Cursing in English on Twitter )


import re
import numpy as np
def Detect_Censorship(textline,censor_list):

    if str(type(textline))!= "<class 'str'>":
        print("the type of the textline should be string")
        return
    
    
    textline = textline.lower()
    textline_kw = " " + textline + " "
    censor_list = [w.lower() for w in censor_list]
    censorship_kw = []
    last_ww = ""

    ######### detecting censorship pattern in the text #########

    ## word-based censorship e.g. f***k (the beginning or ending letter has to appear, unless already included in the curse list e.g., f***, however, for h***, 
    # we only have heck or hell in the curse list, then it has to be h**k, or h**l)
    # we did not consider items containing # and @ except if they are in the censorship keyword list

    for w in censor_list:
        if not (w[-1].isalpha() or w[-1].isnumeric()) and (w[0].isalpha() or w[0].isnumeric()): # if so, we need to add \\ to the ending symbol for the regular expression search e.g. '$','.','*', '(','+','"',"'","@"
            # for each of the case pattern, we added " " in front, to ensure that the detected item is not part of some words, e.g., we want a's -- ass, but not Tiana's 
            censor_cases = [w.group() for w in re.finditer(" "+w[0]+"(.){"+str(len(w)-2)+"}\\"+w[-1]+"[ ,?!;.]",textline_kw)] # the searched pattern has the same first and last letter as the key cursing word w, with the same word length
            censor_start = [w.start() for w in re.finditer(" "+w[0]+"(.){"+str(len(w)-2)+"}\\"+w[-1]+"[ ,?!;.]",textline_kw)]
            censor_end = [w.end() for w in re.finditer(" "+w[0]+"(.){"+str(len(w)-2)+"}\\"+w[-1]+"[ ,?!;.]",textline_kw)]
        elif (w[-1].isalpha() or w[-1].isnumeric()) and not (w[0].isalpha() or w[0].isnumeric()): # if so, we need to add \\ to the starting symbol for the regular expression search
            censor_cases = [w.group() for w in re.finditer(" "+"\\"+w[0]+"(.){"+str(len(w)-2)+"}"+w[-1]+"[ ,?!;.]",textline_kw)]
            censor_start = [w.start() for w in re.finditer(" "+"\\"+w[0]+"(.){"+str(len(w)-2)+"}"+w[-1]+"[ ,?!;.]",textline_kw)]
            censor_end = [w.end() for w in re.finditer(" "+"\\"+w[0]+"(.){"+str(len(w)-2)+"}"+w[-1]+"[ ,?!;.]",textline_kw)]
        elif not (w[-1].isalpha() or w[-1].isnumeric()) and not (w[0].isalpha() or w[0].isnumeric()): # if so, we need to add \\ to both the beginning and ending symbol for the regular expression search
            censor_cases = [w.group() for w in re.finditer(" "+"\\"+w[0]+"(.){"+str(len(w)-2)+"}\\"+w[-1]+"[ ,?!;.]",textline_kw)]
            censor_start = [w.start() for w in re.finditer(" "+"\\"+w[0]+"(.){"+str(len(w)-2)+"}\\"+w[-1]+"[ ,?!;.]",textline_kw)]
            censor_end = [w.end() for w in re.finditer(" "+"\\"+w[0]+"(.){"+str(len(w)-2)+"}\\"+w[-1]+"[ ,?!;.]",textline_kw)]
        else:
            censor_cases = [w.group() for w in re.finditer(r" "+w[0]+"(.){"+str(len(w)-2)+"}"+w[-1]+"[ ,?!;.]",textline_kw)]
            censor_start = [w.start() for w in re.finditer(r" "+w[0]+"(.){"+str(len(w)-2)+"}"+w[-1]+"[ ,?!;.]",textline_kw)]
            censor_end = [w.end() for w in re.finditer(r" "+w[0]+"(.){"+str(len(w)-2)+"}"+w[-1]+"[ ,?!;.]",textline_kw)]
        for w_index in range(len(censor_cases)): #go through every detected cases
            ww = censor_cases[w_index]
            # this is to remove the " " in front of the detected item, so that we can focus only on the exact content of the detected item 
            ww = ww[1:]
            ww_letter = [i for i in range(len(ww)) if ww[i].isalpha()] # for the detected cases, their english letter parts if any has to be exactly the same as the original cursing word
            if len([i for i in ww_letter if ww[i]==w[i]])==len(ww_letter):
                ww_symbol = [i for i in range(len(ww)-1) if (not ww[i].isalpha() and ww[i] != " ")]
                w_symbol = [i for i in ww_symbol if (ww[i] in ["_","%","-",".","#","\\","’","'"] or ww[i]==w[i])] # for the detected cases, their symbol/nonenglish parts if any has to be exactly the same as the original cursing word or from the symbol list ["_","%","-",".","#","\\","’","'"] provided by Wenbo Wang et.al (2014)
                if (len(ww_symbol)==len(w_symbol) and len(ww_symbol)!=0 and (ww[:-1] != last_ww[:-1])): #the comparison with last_ww can avoid repeating counting the exactly same censorship in a row
                    if len([i for i in range(len(w)) if w[i] == " "])!=0: # finally check the blank, if there is blank in the cursing keyword, then the exactly same position the detected cases has to be blank as well
                        w_blank = [i for i in range(len(w)) if w[i] == " "]
                        if len([i for i in w_blank if ww[i]==" "])==len(w_blank):
                                censorship_kw = censorship_kw + [ww] # count it in if the detected case matches all above criterion
                                textline_kw = list(textline_kw) # eliminate the detected case from the list to avoid repeated counting by other cursing keyword (e.g. f**k, fuck)
                                textline_kw[censor_start[w_index]:censor_end[w_index]] = "".join(["t" for t in range((len(ww)))])
                                textline_kw = "".join(textline_kw)
                                last_ww = ww # last_ww is to avoid repetitively counting the exactly same censorship in a row
                                last_end = censor_end[w_index]
                    else: # when cursing keyword does not have the blank/space in it
                        censorship_kw = censorship_kw + [ww]
                        textline_kw = list(textline_kw)
                        textline_kw[censor_start[w_index]:censor_end[w_index]] = "".join(["t" for t in range((len(ww)))])
                        textline_kw = "".join(textline_kw)
                        last_ww = ww # last_ww is to avoid repetitively counting the exactly same censorship in a row
                        last_end = censor_end[w_index]
                elif (len(ww_symbol)==len(w_symbol) and len(ww_symbol)!=0 and ww[:-1] == last_ww[:-1]): #if exactly same censorship in a row appears we still need to replace it to avoid other similar cursing keyword (e.g. f**k, fuck) double counting and update last_ww to avoid another same one in a row (e.g. f**k f**k f**k)
                    textline_kw = list(textline_kw)
                    textline_kw[censor_start[w_index]:censor_end[w_index]] = "".join(["t" for t in range((len(ww)))])
                    textline_kw = "".join(textline_kw)
                    mid = list(set(textline_kw[last_end:censor_start[w_index]]))
                    if len([w for w in mid if w!=" "])>1 or len([w for w in mid if w!=" "])==1: #we do not count repeatedly only when what separated two cases is space/blank, e.g. f**k   f**k, not when there is any other letters/words in between we count e.g. f**k and f**k
                      censorship_kw = censorship_kw + [ww]
                      last_ww = ww
                      last_end = censor_end[w_index]
                    else:
                      last_ww = ww
                      last_end = censor_end[w_index]
                else: #if there is no censorship in a row last_ww returns back to "" to avoid wrongly counting repetition e.g. f**k and f**k the second f**k shall not be deleted from counting 
                    last_ww = ""


    ## search for symbol-based censorship
    textline = textline.split()
    wordlist = []

    # we did not consider items containing # and @ in symbol-based censorship
    # pre-processing the text
    for w in textline:
        if ("#" in w) or ("http:" in w) or ("https:" in w) or ("@" in w) or ("RT" in w):
            wordlist = wordlist + ["tplandrea"]
        else:
            wordlist = wordlist + [w]

    textline = " ".join(wordlist) + "\n"

    rep_vq = 0


    vq_sb = re.compile(r"([\$\(\<\>\)\{\}\[\]\+\-\'\;\.\$\!\?\%\^\&\*\~\=\_\/]){4,}\1*")
    vq_sb_rep = [w.group() for w in vq_sb.finditer(textline)]
    vq_sb_rep_new = vq_sb_rep.copy()
    for cs_temp in vq_sb_rep: ## delete symbol repetition for more than twice so we only allow $$!?, but $$$!?
        if "!?!" in cs_temp or "?!?" in cs_temp or "!??" in cs_temp or "??!" in cs_temp or "!!?" in cs_temp or "?!!" in cs_temp:
            vq_sb_rep_new.remove(cs_temp)
        else:
            break_count = 0 # if one key has three repetition then we break the loop directly no need to check the second key
            for key in list(set(cs_temp)):
                if break_count == 1:
                    break
                count_temp = [i for i, x in enumerate(cs_temp) if x == key]
                if len(count_temp)>2:
                    for i in count_temp:
                        if (i+2) in count_temp and (i+1) in count_temp: #if there are two consecutive symbols are the same, their index diff would be one
                            vq_sb_rep_new.remove(cs_temp)
                            break_count = 1
                            break

    censorship_len = len(censorship_kw) + len(vq_sb_rep_new)
    return censorship_len





