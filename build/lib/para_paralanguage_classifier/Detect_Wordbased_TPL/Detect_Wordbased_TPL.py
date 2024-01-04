##### main function: Detect_Wordbased_TPL (detection of TPL elements that are word / phrase based, including VQ stress, pitch, tempo, emphasis, VS alternants, differentiators, TK alphahaptics)
from .separate_str import separate_str
from .check_tempo import check_tempo
from .check_emphasis import check_emphasis
from .check_pitch import check_pitch
from .check_stress import check_stress
#import enchant
import pkg_resources
import re 
def Detect_Wordbased_TPL(textline, keyword_dic =None,acron_list=None, brown_dic=None):
    
    if str(type(textline))!= "<class 'str'>":
        print("the type of the textline should be string")
        return

    if str(type(keyword_dic))!= "<class 'dict'>":
        print("the type of the textline should be dic")
        return

    if str(type(acron_list))!= "<class 'list'>":
        print("the type of the textline should be list")
        return
    
    if keyword_dic is None: 
        keyword_no_symbol_path = pkg_resources.resource_filename(
                    'para_paralanguage_classifier', 'TPL_support_files/Keyword List_Without Symbol.xlsx')
        word_list = pd.read_excel(keyword_no_symbol_path)  # "TPL_support_files/Keyword List_Without Symbol.xlsx"

        word_list.function[word_list.function == "Detect_Alternants"] = 'alternant'
        word_list.function[word_list.function == "Detect_Differentiators"] = 'differentiator'
        word_list.function[word_list.function == "Detect_alphahaptics"] = 'alphahaptics'

        keyword_dic = word_list.groupby('function')['keywords'].apply(lambda x: x.values.tolist()).to_dict()

    if acron_list is None: 
        acron_path = pkg_resources.resource_filename(
                    'para_paralanguage_classifier', 'TPL_support_files/Excluded Acronyms.xlsx')
        acron_list = pd.read_excel(acron_path) # "TPL_support_files/Excluded Acronyms.xlsx"
        acron_list = list(acron_list.loc[:,"Acronyms"])
        acron_list = acron_list + [w+"s" for w in acron_list]    


    if brown_dic is None:
        brown_dic = set(brown.words())
    # Notation -
    # word_list refers to Andrea's key word list
    # wordlist refers to a list of words waiting for check
    # separate textline by space 
    # letter repetition for elongation and other pattern detection has to be more than or equal to 3 times - DEEEEllicious not okay, DEEEElllicious okay 

    wordlist = re.split(' ',textline)

    ######### pre-processed the key word list #############
    # since we are going to tease out the symbols in text, we also no need for symbols in word list
    word_list = [v for v in keyword_dic.values()]
    word_list = [item for sublist in word_list for item in sublist]
    word_list = [w.lower() for w in word_list]
    word_list = [re.sub(r"[-]","",w) for w in word_list]
    phrase_list = [w for w in word_list if " " in w]
    word_list = [w for w in word_list if w not in phrase_list]
    phraseword_list = [w.split() for w in phrase_list]
    phraseword_list = [item for sublist in phraseword_list for item in sublist]

    alternant_list = keyword_dic["alternant"]
    alternant_list = [w.lower() for w in alternant_list]
    alternant_list = [re.sub(r"[-]","",w) for w in alternant_list]
    phrase_alternant_list = [w for w in alternant_list if " " in w]
    alternant_list = [w for w in alternant_list if w not in phrase_alternant_list]

    differentiator_list =  keyword_dic["differentiator"]
    differentiator_list = [w.lower() for w in differentiator_list]
    differentiator_list = [re.sub(r"[-]","",w) for w in differentiator_list]
    phrase_differentiator_list = [w for w in differentiator_list if " " in w]
    differentiator_list = [w for w in differentiator_list if w not in phrase_differentiator_list]


    alphahaptics_list =  keyword_dic["alphahaptics"]
    alphahaptics_list = [w.lower() for w in alphahaptics_list]
    alphahaptics_list = [re.sub(r"[-]","",w) for w in alphahaptics_list]
    phrase_alphahaptics_list = [w for w in alphahaptics_list if " " in w]
    alphahaptics_list = [w for w in alphahaptics_list if w not in phrase_alphahaptics_list]


    ######### pre-processed the input text #############
    # separate string with symbols
    # two cases, 1 y!a!y, removing the symbols it becomes an english word, 2 *love*this*world, separating by the symbols returns a set of english words
    split_case1 = []
    split_case2 = []
    wordlist_ns = []
    
    for w in wordlist:
        split_case_1 = []
        split_case_2 = [] 
        if ("#" not in w) and ("http:" not in w) and ("https:" not in w) and ("@" not in w) and ("RT" not in w):
            # capture *love*this*world -- [love,this,world], boo#hoo# -- [boo,hoo] when the phrase is keyword
            split_case_1 = separate_str([w], word_list, brown_dic)
            split_case_1 = [w for w in split_case_1 if w!=""]
            # capture ah-mazing, y!a!y
            if len(split_case_1)==0:
                split_case_2 = re.split(r"[^a-zA-Z]",w)
                split_case_2 = ["".join(split_case_2)]
                split_case_2 = [w for w in split_case_2 if w!=""]
            if len(split_case_1)==0 and len(split_case_2)==0:
                wordlist_ns = wordlist_ns + [w]
            else:
                wordlist_ns = wordlist_ns + split_case_1 + split_case_2
        elif ("#" in w) or ("http:" in w) or ("https:" in w) or ("@" in w) or ("RT" in w):
            wordlist_ns = wordlist_ns + ["tplandrea"]

    wordlist = [w for w in wordlist_ns if w!=""]
    
    tempo_case = []
    tempo_count = 0
    tempo_intst_count = 0 # intst - intensity
    emphasis_case = []
    emphasis_count = 0
    emphasis_intst_count = 0 # intst - intensity
    alternant_case = []
    alphahaptics_case = []
    differentiator_case = []
    tpl_case = []   # containing words with tempo or emphasis for detecting stress or pitch later
    en_case = []    # containing English words or key words for detecting stress or pitch later
    phrase_text = [] # containing a new text without tempo or emphasis to detect phrase keyword later

    ######### word-based TPL detecting #############

    
    k = 0
    last_w = 0
    tempo_temp = [" "]
    emphasis_temp = [" "]
    #eng_dic = enchant.Dict("en_US")

    # detecting keyword is conducted in an iterative word by word loop
    for w in wordlist:
        # first we do not repeat counting elements that show up in a row e.g. longggg longggg longggg only the first one counts as tempo, the repetition pattern would be captured by other module called emphasis, tempo only captures pattern within its own word
        if w != "tplandrea" and w!=last_w:
            # raw check see if w is keyword or english word
            if w.lower() in alternant_list: # check alternant case
                alternant_case = alternant_case + [w]
            if w.lower() in differentiator_list: # check differentiator case
                differentiator_case = differentiator_case + [w]
            if w.lower() in alphahaptics_list: # check alphahaptics case
                alphahaptics_case = alphahaptics_case + [w]
            if w.lower() in brown_dic or w.lower() in word_list:  # save for detecting stress or pitch later
                en_case = en_case + [w]
                phrase_text = phrase_text + [w]
            else: # check tempo pattern
                tempo_temp = check_tempo([w], alternant_list, "keyword",brown_dic) # check alternant cases with tempo
                alternant_case = alternant_case + tempo_temp
                tempo_temp = check_tempo([w], differentiator_list, "keyword",brown_dic) # check differentiator cases with tempo
                differentiator_case = differentiator_case + tempo_temp
                tempo_temp = check_tempo([w], alphahaptics_list, "keyword",brown_dic)  # check alphahaptics cases with tempo
                alphahaptics_case = alphahaptics_case + tempo_temp
                phrase_temp = check_tempo([w], phraseword_list,"keyword",brown_dic)  # create a new text without tempo for detecting phrase keyword later
                if len(phrase_temp)>0:
                    phrase_text = phrase_text + phrase_temp
                else:
                    phrase_text = phrase_text + [w] # even if w is not keyword phrase, we still maintain in phrase_text to keep the original text structure
                tempo_temp = check_tempo([w], word_list+phraseword_list,"normal",brown_dic) # check tempo case
                if len(tempo_temp[0])>0:
                    tempo_case = tempo_case + [w]
                    tempo_count = tempo_count + tempo_temp[0][0]
                    tempo_intst_count = tempo_intst_count + tempo_temp[1][0]
                    tpl_case = tpl_case + [w]   # keep tpl tempo case for detecting stress or pitch later
                else:
                    emphasis_temp = check_emphasis([w], alternant_list, "keyword",brown_dic) # check alternant cases with emphasis
                    alternant_case = alternant_case + emphasis_temp
                    emphasis_temp = check_emphasis([w], differentiator_list, "keyword",brown_dic) # check differentiator cases with emphasis
                    differentiator_case = differentiator_case + emphasis_temp
                    emphasis_temp = check_emphasis([w], alphahaptics_list, "keyword",brown_dic)  # check alphahaptics cases with emphasis
                    alphahaptics_case = alphahaptics_case + emphasis_temp
                    phrase_temp = check_emphasis([w], phraseword_list,"keyword",brown_dic) # create a new text without emphasis for detecting phrase keyword later
                    if len(phrase_temp)>0:
                        phrase_text = phrase_text + phrase_temp
                    else:
                        phrase_text = phrase_text + [w] # even if w is not keyword phrase, we still maintain in phrase_text to keep the original text structure
                    emphasis_temp = check_emphasis([w], word_list+phraseword_list, "normal",brown_dic) # check emphasis case
                    if len(emphasis_temp[0])>0:
                        emphasis_case = emphasis_case + [w]
                        emphasis_count = emphasis_count + emphasis_temp[0][0]
                        emphasis_intst_count = emphasis_intst_count + emphasis_temp[1][0]
                        tpl_case = tpl_case + [w] # keep tpl emphasis case for detecting stress or pitch later
        elif w != "tplandrea" and w==last_w:
            phrase_text = phrase_text + [phrase_text[-1]]
        elif w=="tplandrea":
            phrase_text = phrase_text + [w]
        last_w = wordlist[k]
        k = k + 1



    # detecting phrase-based keyword is conducted by checking through the whole sentence
    phrase_case = []
    phrase_text = " ".join(phrase_text) # change the word list (one without tempo and emphasis) into a text
    phrase_text = phrase_text.lower()
    for phrase in phrase_list: # match phrase kw in the new text one after another using regular expression
        phrase_temp = [w.start() for w in re.finditer(phrase,phrase_text)]
        phrase_temp_new = phrase_temp.copy() # delete repeated occurance in a row e.g. boo hoo boo hoo boo hoo
        if len(phrase_temp)>2 or len(phrase_temp) == 2:
            for i in range(len(phrase_temp)-1): # we do not need to do the examination for the last one
                if phrase_text[(phrase_temp[i]+len(phrase)+1):(phrase_temp[i]+2*len(phrase)+1)] == phrase:
                    phrase_temp_new.remove(phrase_temp[i])
            if phrase in phrase_alternant_list: # check alternant phrase cases
                alternant_case = alternant_case + [phrase]*len(phrase_temp_new)
            if phrase in phrase_differentiator_list:  # check differentiator phrase cases
                differentiator_case = differentiator_case + [phrase]*len(phrase_temp_new)
            if phrase in phrase_alphahaptics_list:
                alphahaptics_case = alphahaptics_case + [phrase]*len(phrase_temp_new)
        elif len(phrase_temp)==1:
            if phrase in phrase_alternant_list:
                alternant_case = alternant_case + [phrase]
            if phrase in phrase_differentiator_list:
                differentiator_case = differentiator_case + [phrase]
            if phrase in phrase_alphahaptics_list:
                alphahaptics_case = alphahaptics_case + [phrase]


     # detecting pitch and stress
    last_w = 0
    pitch_case = []
    pitch_temp = []
    for w in wordlist:
        if w != "tplandrea" and (w in en_case or w in tpl_case):
            pitch_temp = check_pitch([w])
            if len(pitch_temp)>0 and last_w == 0:
                pitch_case = pitch_case + [w]
            elif w.isupper() and len(w) == 1 and last_w != 0:
                pitch_temp = ["temp"]
        elif (w.isupper() and last_w != 0) or w in ["&",".",",","?","!",":",";","$","(",")","[","]","|","{","}","<",">"]:
            pitch_temp = ["temp"]
        else:
            pitch_temp = []
        last_w = len(pitch_temp)


    last_w = 0
    stress_case = []
    stress_temp = []
    for w in wordlist:
        if w != "tplandrea" and (w in en_case or w in tpl_case):
            stress_temp = check_stress([w],acron_list)
            if len(stress_temp)>0 and last_w == 0: # last_w is to avoid duplicated counting stress
                stress_case = stress_case + [w]
            elif w.isupper() and last_w != 0:
                stress_temp = ["temp"]
        elif (w.isupper() and last_w != 0) or w in ["&",".",",","?","!",":",";","$","(",")","[","]","|","{","}","<",">"]:
            stress_temp = ["temp"]
        else:
            stress_temp = []
        last_w = len(stress_temp)
    


    return len(stress_case), len(pitch_case),tempo_count,emphasis_count,len(alternant_case),len(differentiator_case), len(alphahaptics_case), tempo_intst_count,emphasis_intst_count

