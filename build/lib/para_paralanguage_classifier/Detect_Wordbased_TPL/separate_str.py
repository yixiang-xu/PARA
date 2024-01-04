##### supporting function: separate_str (delete symbols in words to make text pure words)

import re
def separate_str(wordlist,word_list, brown_dic):

    if str(type(wordlist))!= "<class 'list'>":
        print("the type of the wordlist should be list")
        return

    if str(type(word_list))!= "<class 'list'>":
        print("the type of the keyword should be list")
        return  


    # change the text into lower case
    word_list = [w.lower() for w in word_list]
    #eng_dic = enchant.Dict("en_US") 
    rhythm_word_list = []

    r1 = re.compile(r'(([a-zA-Z])([^a-zA-Z0-9]))')

    # check for those string with symbols in between, whether or not string should be separated by symbols into a set of words the criterion is whether or not those separated elements are English words
    for word in wordlist:
        rep_pattern = r1.findall(word)
        if len(rep_pattern)!=0:
            w_count = 0
            word_ns = re.split(r"[^a-zA-Z0-9]", word)
            word_ns = [w for w in word_ns if w !="" and w!=" "]
            for w in word_ns:
                if (w.lower() in brown_dic or w.lower() in word_list) and len(w)>1:
                    w_count = w_count + 1
        # only when the # true english check matches the # of words
            if w_count == len(word_ns) and len(set(word_ns))!=1:
                rhythm_word_list = rhythm_word_list  + word_ns
            else:
                word_ns_new = " ".join(word_ns)
                if word_ns_new in word_list:
                    rhythm_word_list = rhythm_word_list + word_ns



    return rhythm_word_list 





            
