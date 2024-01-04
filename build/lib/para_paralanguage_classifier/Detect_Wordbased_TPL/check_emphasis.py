##### supporting function: check_emphasis (detect emphasis TPL pattern word by word), e.g. wowowow, coolcoolcool

#import enchant
import re 
def check_emphasis(wordlist, word_list,type, brown_dic):

    new_word_list = []
    new_word_count_list = []

    #eng_dic = enchant.Dict("en_US")
    
    ## word by word check the emphasis pattern
    for word in wordlist:      
        r = re.compile(r"([^0-9]+?)\1+") # this will get the smallest repetition (at least two repetition to be counted)
        # check repeated letter 
        l_rep = r.findall(word) # return root units e.g. wow, cool
        count_rep = [w.group() for w in r.finditer(word)] # this return the whole that contains the root, to count the repetition
        if len(l_rep)!=0:
            for i in range(len(l_rep)): # if wowwow, then unit is wow
                r = l_rep[i]
                # "normal" stands for check emphasis this element
                if type == "normal":
                    emphasis_rep = len(count_rep[i])/len(r)
                    if r.lower() in brown_dic and len(r)>1:
                        new_word_list = new_word_list + [emphasis_rep/3 if emphasis_rep/3>=1 else 0 for w in [1]] # repetition counts every 3 as one unit and has to at least three
                        new_word_count_list = new_word_count_list + [1 if emphasis_rep/3>=1 else 0 for w in [1]] # repetition counts as just one unit as long as there is three repetition
                    elif r.lower() in word_list and len(r)>1:
                        new_word_list = new_word_list + [max(1,emphasis_rep/3)] # repetition counts every 3 as one unit otherwise one for less than three repetition (i.e. two repetition) only for keyword
                        new_word_count_list = new_word_count_list + [1] # repetition counts regardless if the length is three repetitions for keywords
                    else:
                        word_new =  r + r[0] # if wowowowow, then unit is wo, then create wow, and this new word_new has to include three repetition minimally 
                        if word_new.lower() in brown_dic and len(set(word_new))>1:
                            new_word_list = new_word_list + [emphasis_rep/3 if emphasis_rep/3>=1 else 0 for w in [1]] #[emphasis_rep/3]
                            new_word_count_list = new_word_count_list + [1 if emphasis_rep/3>=1 else 0 for w in [1]] 
                        elif word_new.lower() in word_list and len(set(word_new))>1: # len(set(word_new))>2 
                            new_word_list = new_word_list + [emphasis_rep/3 if emphasis_rep/3>=1 else 0 for w in [1]]  #[emphasis_rep/3]
                            new_word_count_list = new_word_count_list + [1 if emphasis_rep/3>=1 else 0 for w in [1]] 
                # "keyword" stands for detection of alternant, differentiator, alphahaptics elements
                elif type == "keyword":
                    if r.lower() in word_list:
                        new_word_list = new_word_list + [r]
                    else:
                        word_new =  r + r[0] # if wowowowow, then unit is wo, then create wow
                        if word_new.lower() in word_list:
                            new_word_list = new_word_list + [word_new]


    return new_word_list if type =="keyword" else [new_word_count_list,new_word_list]

