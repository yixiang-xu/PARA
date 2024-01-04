##### supporting function: check_tempo (detect tempo TPL pattern word by word), e.g. wowwwwww

#import enchant
import re
from itertools import product
def check_tempo(wordlist, word_list,type, brown_dic):
    
    new_word_list = []
    new_word_count_list = []
    #eng_dic = enchant.Dict("en_US")
    word_list = [w.lower() for w in word_list]
    
    for word in wordlist:
        word_rep = word.lower()
        # "keyword" stands for detection of alternant, differentiator, alphahaptics elements
        if type == "keyword": # tempo elongation has to be at least two reptition
            r = re.compile(r"([a-z])\1{1,}")
        # "normal" stands for check tempo this element
        elif type == "normal": # elongation has to be at least three reptition
            r = re.compile(r"([a-z])\1{2,}")
        elongation_list = [w.group() for w in r.finditer(word_rep)]
        rep = r.findall(word_rep)
        nrep = len(rep)
        reduced_letter_cases = list(product('12', repeat=nrep))

        if nrep!=0 and len(set(word))>1: # not single letter
            ### reduce all the letter repetition into either one or two
            for i in range(len(reduced_letter_cases)):
                word_new = word_rep
                # creating new word by shortening the elongation to either one or two
                for j in range(len(elongation_list)):
                    word_new = word_new.replace(elongation_list[j], rep[j]*int(reduced_letter_cases[i][j]), 1)
                if type == "keyword":
                    if word_new in word_list:
                        new_word_list = new_word_list + [word_new]
                        break
                elif type == "normal":
                    tempo_rep = sum([len(w) for w in elongation_list]) #sum([len(w)/3 for w in elongation_list]) # repetition counts every 3 as one unit - for intensity score of tempo
                    tempo_rep_count = 1 # regardless of how many elongation samples, it count as one as long as there is any - for pure count of tempo
                    if word_new in brown_dic:
                        new_word_list = new_word_list + [tempo_rep]
                        new_word_count_list = new_word_count_list + [tempo_rep_count]
                        break
                    elif word_new in word_list:
                        new_word_list = new_word_list + [tempo_rep]
                        new_word_count_list = new_word_count_list + [tempo_rep_count]
                        break
                    elif len(re.findall(r"([a-z])\1{4,}",word_rep)):
                        new_word_list = new_word_list + [tempo_rep]
                        new_word_count_list = new_word_count_list + [tempo_rep_count]
                        break
                    elif word[0].isupper():
                        word_new = word_new.title()
                        if word_new in brown_dic:
                            new_word_list = new_word_list + [tempo_rep]
                            new_word_count_list = new_word_count_list + [tempo_rep_count]
                            break
        elif len(set(word))==1 and len(re.findall(r"([a-z])\1{4,}",word_rep)) and type == "normal": #we will count single letter with at least 4 elongation
            rr = re.compile(r"([a-z])\1{4,}")
            elongation_list = [w.group() for w in rr.finditer(word_rep)]
            tempo_rep = sum([len(w) for w in elongation_list])  #sum([len(w)/3 for w in elongation_list]) # repetition counts every 3 as one unit - for intensity score of tempo
            new_word_list = new_word_list + [tempo_rep]
            tempo_rep_count = 1 # regardless of how many elongation samples, it count as one as long as there is any - for pure count of tempo
            new_word_count_list = new_word_count_list + [tempo_rep_count]
                


    return new_word_list if type == "keyword" else [new_word_count_list, new_word_list]
         
       
