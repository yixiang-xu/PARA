##### secondary supporting function: block_emoticon (detect emoticon TPL pattern under strict rules)
import re 


def block_emoticon(emoticon_list, textline):
    
    mt_list_total = []
    mt_span_total = []
    mt_intst_count = []
    mt_count = []
    for k in emoticon_list:
        k_hat = ""
        # this loop adds symbol \\ in front of non digit non english letter symbol in those emoticon 
        for sym in k:
            if len(re.findall(r"[0-9A-Za-z]",sym))!=0:
                k_hat = k_hat + sym
            else:
                k_hat = k_hat + "\\"+ sym
        ## detect any (consecutive) emoticon pattern -- emoticon{space}emoticon the space and the second one is optional  ##
        if len(re.findall("("+k_hat+"\\s?)\\1*"+"("+k_hat+")?",textline))!=0:
            mt_span = list(re.finditer("("+k_hat+"\\s?)\\1*"+"("+k_hat+")?",textline))
            # we add ("+k_hat+")?" so to avoid having matched emoticon pattern ending with whitespace which will mess up the later checking of the restricted rules
            mt_span = [w.span() for w in mt_span]
            for i in range(len(mt_span)):
                if textline[mt_span[i][1]-1]==" ":
                    mt_span[i] = (mt_span[i][0],mt_span[i][1]-1)
            i = 0
            while i<len(mt_span)-1: # merge detected emoticon patterns of which positions are next and separated by whitespace
                mt_between = list(set(textline[mt_span[i][1]:mt_span[i+1][0]])) # check what is in between
                if mt_between == [" "] or mt_between == []: # if nothing in between or only whitespace
                    mt_span = mt_span[:i] + [(mt_span[i][0],mt_span[i+1][1])] + mt_span[i+1+1:]
                    i = 0
                else:
                    i = i + 1
            mt_text = [textline[w[0]:w[1]] for w in mt_span] 
            mt_text = [re.findall("("+k_hat+")",w) for w in mt_text]
            mt_list = mt_text.copy()
            mt_span_temp = mt_span
            #####################################
            ## check based on restricted rules ##
        #rule 1#  check if the k-hat has a left parenthesis, and if so, the side should not has a right parenthesis #this check is orthogonal to check 1
            if re.findall("\\(",k_hat) and not re.findall("\\)",k_hat):
                for i in range(len(mt_span)):
                    ii = mt_span[i][1]
                    if i+1 < len(mt_span): #if i is the ones but the last identified emoticon, then going through the text till reaching the next identified emoticon
                        while ii < mt_span[i+1][0]:
                            if textline[ii] ==")":
                                if k in mt_list[i]:
                                    mt_list[i].remove(k)
                                    mt_span_temp = [w for w in mt_span_temp if w != mt_span[i]]
                                    break
                            else:
                                ii = ii + 1
                    elif i+1 >= len(mt_span): #if i is the last identified emoticon, then going through to the end of text
                        while ii < len(textline):
                            if textline[ii] ==")":
                                if k in mt_list[i]:
                                    mt_list[i].remove(k)
                                    mt_span_temp = [w for w in mt_span_temp if w != mt_span[i]]
                                    break
                            else:
                                ii = ii + 1
            mt_span = mt_span_temp
        #rule 2#   check if the k-hat has a right parenthesis, and if so, the side should not has a left parentheis #this check is orthogonal to check 1 and 2 
            if re.findall("\\)",k_hat) and not re.findall("\\(",k_hat):
                for i in range(len(mt_span)-1,-1,-1):
                    if mt_span[i][0]-1>=0:
                        ii = mt_span[i][0]-1
                        if i-1 >= 0: # if i is the ones but the first identified emoticon, then going through the text till reaching the previous identified emoticon
                            while ii> mt_span[i-1][1] or ii==mt_span[i-1][1]:
                                if textline[ii] =="(":
                                    if k in mt_list[i]:
                                        mt_list[i].remove(k)
                                        mt_span_temp = [w for w in mt_span_temp if w != mt_span[i]]
                                        break
                                else:
                                    ii = ii - 1
                        elif i-1 < 0 : # if i is the first identified emoticon then going to the rest of text
                            while ii > 0 or ii==0: # going through to the first element in the text
                                if textline[ii] =="(":
                                    if k in mt_list[i]:
                                        mt_list[i].remove(k)
                                        mt_span_temp = [w for w in mt_span_temp if w != mt_span[i]]
                                        break
                                else:
                                    ii = ii - 1
            mt_span = mt_span_temp
            k_hat = re.sub(r'\\','',k_hat) # in order to return to the original emoticon format (we needed \\ before, for regular expression search works)
        #rule 3#  check if the k-hat has number at the left end or symbol ":"  or "=" -- this is to rule out 1:3, or 0:0, 3=3
            # if so the character prior to the left end of the k-hat has to be non number
            if (k_hat[0].isdigit()) or (k_hat[0]==':') or (k_hat[0]=='='):
                for i in range(len(mt_span)):
                    if mt_span[i][0]-1>=0:
                        if (textline[mt_span[i][0]-1].isdigit()) or (textline[mt_span[i][0]-1].isalpha()):
                            if k in mt_list[i]:
                                mt_list[i].remove(k)
                            mt_span_temp = [w for w in mt_span_temp if w != mt_span[i]]
            mt_span = mt_span_temp
        #rule 4#  check if the k-hat has number at the right end  or symbol ":"  or "=" 
            # if so the character after the right end of the k-hat has to be non number
            if k_hat[-1].isdigit() or (k_hat[-1]==':') or (k_hat[-1]=='='):
                for i in range(len(mt_span)):
                    if mt_span[i][1] < len(textline):
                        if textline[mt_span[i][1]].isdigit() or textline[mt_span[i][0]-1].isalpha():
                            if k in mt_list[i]:
                                mt_list[i].remove(k)
                            mt_span_temp = [w for w in mt_span_temp if w != mt_span[i]]
            mt_span = mt_span_temp
        #rule 5#  check if the k-hat has letter at the left end (no wory about right end because of the space in regular expression),
            # if so the character prior to the left end of the k-hat has to be non letter
            if k_hat[0].isalpha():
                for i in range(len(mt_span)):
                    if mt_span[i][0]-1>=0:
                        if textline[mt_span[i][0]-1].isalpha() or textline[mt_span[i][0]-1].isdigit():
                            if k in mt_list[i]:
                                mt_list[i].remove(k)
                            mt_span_temp = [w for w in mt_span_temp if w != mt_span[i]]
            mt_span = mt_span_temp
        #rule 6#  check if the k-hat has letter at the right end 
            # if so the character after the right end of the k-hat has to be non letter
            if k_hat[-1].isalpha():
                for i in range(len(mt_span)):
                    if mt_span[i][1] < len(textline):
                        if textline[mt_span[i][1]].isalpha() or textline[mt_span[i][1]].isdigit():
                            if k in mt_list[i]:
                                mt_list[i].remove(k)
                            mt_span_temp = [w for w in mt_span_temp if w != mt_span[i]]
            mt_span = mt_span_temp
            for pr in mt_span:
                textline = textline[:pr[0]] + 'A'*(pr[1]-pr[0]) + textline[pr[1]:]
            mt_list_total = mt_list_total + mt_list
            mt_span_total = mt_span_total + mt_span
    for i in range(len(mt_list_total)):
        mt_rep = len(mt_list_total[i]) # count the number of emoticon repetition
        if mt_rep >0:
            mt_intst_count.append(mt_rep)
            mt_count.append(1)
        else:
            mt_count.append(0)


        # if mt_rep >3 or mt_rep==3:
        #     mt_intst_count.append(mt_rep/3)
        #     mt_count.append(1)
        # elif mt_rep >0 and mt_rep<3:
        #     mt_intst_count.append(1)
        #     mt_count.append(1)
        # else:
        #     mt_count.append(0)


    return mt_span_total, sum(mt_count), sum(mt_intst_count)


