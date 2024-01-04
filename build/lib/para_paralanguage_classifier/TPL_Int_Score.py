import os 
import pandas as pd 
import re 
import sys 
import numpy as np
import regex
from collections import Counter
from .Detect_Wordbased_TPL import Detect_Wordbased_TPL
from .Detect_Silence import Detect_Silence
from .Detect_Emphasis import Detect_Emphasis
from .Detect_Asterisk_TPL import Detect_Asterisk_TPL
from .Detect_Rhythm import Detect_Rhythm
from .Detect_Censorship import Detect_Censorship
from .Detect_Spelling import Detect_Spelling
from .Detect_Emojicon_TPL import Detect_Emojicon_TPL
from .Detect_Formatting import Detect_Formatting
from nltk.corpus import brown
from multiprocessing import Process
import traceback
import pkg_resources
import functools


class prep:
    def __init__(self, 
                 keyword_no_symbol_path=None, 
                 acron_path=None,
                 keyword_symbol_path=None, 
                 curse_path=None, 
                 emoticon_a_path=None, 
                 emoticon_vk_path=None, 
                 emoticon_tk_path=None,
                 emoji_path=None, 
                 brown_dic=None):


        self.keyword_no_symbol_path = keyword_no_symbol_path
        self.acron_path = acron_path
        self.keyword_symbol_path = keyword_symbol_path
        self.curse_path = curse_path
        self.emoticon_a_path = emoticon_a_path
        self.emoticon_tk_path = emoticon_tk_path
        self.emoticon_vk_path = emoticon_vk_path
        self.emoji_path = emoji_path
        self.brown_dic = brown_dic

        if keyword_no_symbol_path is None: 
            self.keyword_no_symbol_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/Keyword List_Without Symbol.xlsx')
        if acron_path is None: 
            self.acron_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/Excluded Acronyms.xlsx')
        if keyword_symbol_path is None: 
            self.keyword_symbol_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/Keyword List_With Symbol.xlsx')
        if curse_path is None: 
            self.curse_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/cursing_lexicon.txt')
        if emoticon_a_path is None: 
            self.emoticon_a_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/emoticon_a.txt')
        if emoticon_vk_path is None: 
            self.emoticon_vk_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/emoticon_vk.txt')
        if emoticon_tk_path is None: 
            self.emoticon_tk_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/emoticon_tk.txt')
        if emoji_path is None: 
            self.emoji_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/Emoji Dictionary.xlsx')
        if brown_dic == None:
            self.brown_dic = set(brown.words())


        self.word_list = pd.read_excel(self.keyword_no_symbol_path)  # "TPL_support_files/Keyword List_Without Symbol.xlsx"

        self.word_list.function[self.word_list.function == "Detect_Alternants"] = 'alternant'
        self.word_list.function[self.word_list.function == "Detect_Differentiators"] = 'differentiator'
        self.word_list.function[self.word_list.function == "Detect_alphahaptics"] = 'alphahaptics'

        self.keyword_dic = self.word_list.groupby('function')['keywords'].apply(lambda x: x.values.tolist()).to_dict()

        self.acron_list = pd.read_excel(self.acron_path) # "TPL_support_files/Excluded Acronyms.xlsx"
        self.acron_list = list(self.acron_list.loc[:,"Acronyms"])
        self.acron_list = self.acron_list + [w+"s" for w in self.acron_list]


        self.word_list_S =  pd.read_excel(self.keyword_symbol_path) #"TPL_support_files/Keyword List_With Symbol.xlsx"
        self.word_list_sb = self.word_list_S.copy()
        self.word_list_sb.function[self.word_list_sb.function=="Detect_Differentiators"] ='vs'
        self.word_list_sb.function[self.word_list_sb.function=="Detect_Volume"] ='vq'
        self.word_list_sb.function[self.word_list_sb.function=="Detect_alphakinesics"] ='vk'
        self.word_list_sb.function[self.word_list_sb.function=="Detect_alphahaptics"] ='tk'

        self.word_list_sb2 = self.word_list_S.copy()
        self.word_list_sb2.function[self.word_list_sb2.function!="Detect_alphakinesics"] ='nvk'
        self.word_list_sb2 = self.word_list_sb2.loc[self.word_list_sb2.function=='nvk',]

        self.word_list_sb3 = self.word_list_S.copy()
        self. word_list_sb3.function ='na'
        self.word_list_sb4 = pd.DataFrame({'TPL':["artifact"], 'keywords':["emoji"], 'function':["a"]})


        self.word_list_sb = pd.concat([self.word_list_sb, self.word_list_sb2,self.word_list_sb3, self.word_list_sb4])
        self.keyword_dic_sb = self.word_list_sb.groupby('function')['keywords'].apply(lambda x: x.values.tolist()).to_dict()


        self.word_list_comb = pd.concat([self.word_list_S, self.word_list], axis=0)
        self.word_list_comb = list(self.word_list_comb.loc[:,"keywords"])
        self.word_list_comb = [w.lower() for w in self.word_list_comb]


        self.censor_list = []
        with open(curse_path, "r", encoding = 'utf-8') as f: #"TPL_support_files/cursing_lexicon.txt"
            for line in f:
                self.censor_list.append(line)
            self.censor_list = [re.sub(r"\n","", w) for w in self.censor_list]



        self.emoticon_a = []
        with open(emoticon_a_path, "r", encoding = 'utf-8') as f: #"TPL_support_files/emoticon_a.txt"
            for line in f:
                self.emoticon_a.append(line)
            self.emoticon_a = [re.sub(r"\n","", w) for w in self.emoticon_a]

        self.emoticon_vk = []
        with open(emoticon_vk_path, "r", encoding = 'utf-8') as f: #"TPL_support_files/emoticon_vk.txt"
            for line in f:
                self.emoticon_vk.append(line)
            self.emoticon_vk = [re.sub(r"\n","", w) for w in self.emoticon_vk]

        self.emoticon_tk = []
        with open(emoticon_tk_path, "r", encoding = 'utf-8') as f: #"TPL_support_files/emoticon_tk.txt"
            for line in f:
                self.emoticon_tk.append(line)
            
            self.emoticon_tk = [re.sub(r"\n","", w) for w in self.emoticon_tk]


        self.key_emoticon = {"a":self.emoticon_a, "na": self.emoticon_vk+ self.emoticon_tk, 
                    "vk":self.emoticon_vk, "nvk": self.emoticon_a + self.emoticon_tk,
                    "tk":self.emoticon_tk, "ntk": self.emoticon_a + self.emoticon_vk}


        self.key_emoji = pd.read_excel(emoji_path) #"TPL_support_files/Emoji Dictionary.xlsx"
        self.key_emoji['TPL'] = self.key_emoji['TPL'].str.lower()
        self.key_emoji = self.key_emoji.groupby('TPL')['Browser'].apply(lambda x: x.values.tolist()).to_dict()
        self.key_emoji['a'] = [w for w in self.key_emoji['a'] if w!='*️⃣']




    def emoticon_hierachy(self, type):
            ### pre-processing emoticon list ###
        if type == "tk":
            target_emoticon = self.key_emoticon["tk"]
        elif type == "vk":
            target_emoticon = self.key_emoticon["vk"]
        elif type == "a":
            target_emoticon = self.key_emoticon["a"]

        if "x" in target_emoticon:
            target_emoticon = [w for w in target_emoticon if (w not in ['x', 'xx', 'xxx', 'XXX', 'XX', 'X'])]


        emoticon = target_emoticon
        
        emoticon_top =[]
        emoticon_mid =[]
        emoticon_mid2 =[]
        emoticon_btm =[]
        # delete any duplication in the emoticon list 
        emoticon = list(set(emoticon))
        emoticon2 = []
        emoticon3 = []
        emoticon4 = []
        
        ### create four-layer hierachy in emoticon due to the nested characteristics of emoticon e.g. :D *:D ###
        # putting \\ before any symbol in the emoticon for the sake of regular expression search
        for k in emoticon: 
            k_hat = ""  
            for i in k:
                if len(re.findall(r"[0-9A-Za-z ]",i))!=0:
                    k_hat = k_hat + i
                else:
                    k_hat = k_hat + "\\"+ i
            # create hierachy in emoticon 
            # the top(leaf) is emoticon only found once in the emoticon list        
            if (len(re.findall(k_hat, " ".join(emoticon))))==1:
                emoticon_top = emoticon_top + [k];
            else:
            # list of emoticon found more than once -- building units of top
                emoticon2 = emoticon2 + [k];

        # putting \\ before any symbol of the building unit of top for search purpose
        for k in emoticon2:
            k_hat = ""
            for i in k:
                if len(re.findall(r"[0-9A-Za-z ]",i))!=0:
                    k_hat = k_hat + i
                else:
                    k_hat = k_hat + "\\"+ i
            # the mid is emoticon found once in the building units list
            if (len(re.findall(k_hat, " ".join(emoticon2))))==1:
                emoticon_mid = emoticon_mid + [k];
            else:
                # emoticon found more than once building units of mid 
                emoticon3 = emoticon3 + [k];

        # putting \\ before any symbol of the building unit of mid for search purpose
        for k in emoticon3:
            k_hat = ""
            for i in k:
                if len(re.findall(r"[0-9A-Za-z ]",i))!=0:
                    k_hat = k_hat + i
                else:
                    k_hat = k_hat + "\\"+ i
            # the mid2 is emoticon found once in the building units of mid list
            if (len(re.findall(k_hat, " ".join(emoticon3))))==1:
                emoticon_mid2 = emoticon_mid2 + [k];
            else:
            # emoticon found more than once in the building units of mid2 list
                emoticon_btm = emoticon_btm + [k];
        return emoticon_top, emoticon_mid2, emoticon_mid, emoticon_btm



def validate_and_run(func):
    @functools.wraps(func)
    def wrapper(self, textline, *args, **kwargs):
        try:
            if not (isinstance(textline, str) and textline.strip()):
                textline = str(textline) + ' '
            return func(self, textline, *args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()

    return wrapper


class para_output:
    def __init__(self, 
        keyword_no_symbol_path =None, 
        acron_path =None,
        keyword_symbol_path = None, 
        curse_path = None, 
        emoticon_a_path = None, 
        emoticon_vk_path = None, 
        emoticon_tk_path = None,
        emoji_path = None, 
        brown_dic =None):


        self.keyword_no_symbol_path = keyword_no_symbol_path
        self.acron_path = acron_path
        self.keyword_symbol_path = keyword_symbol_path
        self.curse_path = curse_path
        self.emoticon_a_path = emoticon_a_path
        self.emoticon_tk_path = emoticon_tk_path
        self.emoticon_vk_path = emoticon_vk_path
        self.emoticon_a_path = emoticon_a_path
        self.emoji_path = emoji_path
        self.brown_dic = brown_dic

        if keyword_no_symbol_path is None: 
            self.keyword_no_symbol_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/Keyword List_Without Symbol.xlsx')
        if acron_path is None: 
            self.acron_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/Excluded Acronyms.xlsx')
        if keyword_symbol_path is None: 
            self.keyword_symbol_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/Keyword List_With Symbol.xlsx')
        if curse_path is None: 
            self.curse_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/cursing_lexicon.txt')
        if emoticon_a_path is None: 
            self.emoticon_a_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/emoticon_a.txt')
        if emoticon_vk_path is None: 
            self.emoticon_vk_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/emoticon_vk.txt')
        if emoticon_tk_path is None: 
            self.emoticon_tk_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/emoticon_tk.txt')
        if emoji_path is None: 
            self.emoji_path = pkg_resources.resource_filename(
                'para_paralanguage_classifier', 'TPL_support_files/Emoji Dictionary.xlsx')
        if brown_dic == None:
            self.brown_dic = set(brown.words())


        self.prep = prep(self.keyword_no_symbol_path, self.acron_path,self.keyword_symbol_path, self.curse_path, self.emoticon_a_path, self.emoticon_vk_path, self.emoticon_tk_path,self.emoji_path, self.brown_dic)
        self.emoticon_hier_tk = self.prep.emoticon_hierachy('tk')
        self.emoticon_hier_vk = self.prep.emoticon_hierachy('vk')
        self.emoticon_hier_a = self.prep.emoticon_hierachy('a')


        self.vq_stress = None
        self.vq_pitch = None
        self.vq_tempo_1 = None 
        self.vq_emphasis_1 = None 
        self.vs_alternants = None 
        self.vs_differentiators_1 = None 
        self.tk_alphahaptics_1 = None 
        self.vq_intst_tempo_1 = None 
        self.vq_intst_emphasis_1 = None 
        self.vq_silence = None 
        self.vq_intst_silence = None 
        self.vq_emphasis_2 = None 
        self.vq_intst_emphasis_2 = None 
        self.vq_volume = None 
        self.vs_differentiators_asterisk = None 
        self.tk_alphahaptics_asterisk = None 
        self.vk_alphakinesics = None 
        self.a_emoji_symbol = None 
        self.vq_rhythm = None 
        self.vq_censorship = None 
        self.vq_spelling = None 
        self.tk_tactileemojis = None 
        self.vk_bodilyemojis = None 
        self.a_nonbodilyemojis = None 
        self.tk_bodilyemoticons = None 
        self.vk_bodilyemoticons = None 
        self.a_nonbodilyemoticons = None 

        self.tk_intst_tactileemojis = None 
        self.vk_intst_bodilyemojis = None 
        self.a_intst_nonbodilyemojis = None 
        self.tk_intst_bodilyemoticons = None 
        self.vk_intst_bodilyemoticons = None 
        self.a_intst_nonbodilyemoticons = None 
        self.a_formatting  = None 

# ------------------------------------------------
#  Building Blocks 
    @validate_and_run
    def _run_wordbased_tpl(self, textline):
        ## Function Detect_Wordbased_TPL
        temp = Detect_Wordbased_TPL(textline, self.prep.keyword_dic, self.prep.acron_list, self.prep.brown_dic)
        self.vq_stress = temp[0]
        self.vq_pitch = temp[1]
        self.vq_tempo_1 = temp[2]
        self.vq_emphasis_1 = temp[3]
        self.vs_alternants = temp[4]
        self.vs_differentiators_1 = temp[5]
        self.tk_alphahaptics_1 = temp[6]
        self.vq_intst_tempo_1 = temp[7]
        self.vq_intst_emphasis_1 = temp[8]

    @validate_and_run
    def _run_silence_tpl(self, textline):
        ## Function Detect_Silence
        temp = Detect_Silence(textline)
        self.vq_silence = temp[0]
        self.vq_intst_silence = temp[1]
 
    @validate_and_run
    def _run_emphasis_tpl(self, textline):
        ## Function Detect_Emphasis
        temp = Detect_Emphasis(textline)
        self.vq_emphasis_2 = temp[0]
        self.vq_intst_emphasis_2 = temp[1]

    @validate_and_run
    def _run_asterisk_tpl(self, textline):
        ## Function Detect_Asterisk_TPL 
        temp = Detect_Asterisk_TPL(textline, self.prep.keyword_dic_sb)
        self.vq_volume = temp[0]
        self.vs_differentiators_asterisk = temp[1]
        self.tk_alphahaptics_asterisk = temp[2]
        self.vk_alphakinesics = temp[3]
        self.a_emoji_symbol = temp[4]

    @validate_and_run
    def _run_rhythm_tpl(self, textline):
        self.vq_rhythm = Detect_Rhythm(textline, self.prep.word_list_comb, self.prep.brown_dic)


    @validate_and_run
    def _run_censorship_tpl(self, textline):
        self.vq_censorship = Detect_Censorship(textline, self.prep.censor_list)

    @validate_and_run
    def _run_spelling_tpl(self, textline):
        self.vq_spelling = Detect_Spelling(textline, self.prep.word_list,self.prep.brown_dic, self.prep.acron_list)

    @validate_and_run
    def _run_emojicon_tpl(self, textline):
        temp = Detect_Emojicon_TPL(textline, self.prep.key_emoji, self.prep.key_emoticon, self.emoticon_hier_tk, self.emoticon_hier_vk, self.emoticon_hier_a )
        self.tk_tactileemojis = temp[0]
        self.vk_bodilyemojis = temp[1]
        self.a_nonbodilyemojis = temp[2]
        self.tk_bodilyemoticons = temp[3]
        self.vk_bodilyemoticons = temp[4]
        self.a_nonbodilyemoticons = temp[5]

        self.tk_intst_tactileemojis = temp[6]
        self.vk_intst_bodilyemojis = temp[7]
        self.a_intst_nonbodilyemojis = temp[8]
        self.tk_intst_bodilyemoticons = temp[9]
        self.vk_intst_bodilyemoticons = temp[10]
        self.a_intst_nonbodilyemoticons = temp[11]

    @validate_and_run
    def _run_formatting_tpl(self, textline):
        self.a_formatting  = Detect_Formatting([textline])


# ------------------------------------------------
#  subcategory level output 
    @validate_and_run
    def compute_vq_pitch(self, textline):
        self._run_wordbased_tpl(textline)
        return {"vq_pitch": self.vq_pitch}

    @validate_and_run
    def compute_vq_rhythm(self, textline):
        self._run_rhythm_tpl(textline)
        return {"vq_rhythm": self.vq_rhythm}

    @validate_and_run
    def compute_vq_stress(self, textline):
        self._run_wordbased_tpl(textline)
        return {"vq_stress": self.vq_stress}

    @validate_and_run
    def compute_vq_emphasis(self, textline):
        self._run_wordbased_tpl(textline)
        self._run_emphasis_tpl(textline)
        return {"vq_emphasis": self.vq_emphasis_1 + self.vq_emphasis_2}


    @validate_and_run
    def compute_vq_tempo(self, textline):
        self._run_wordbased_tpl(textline)
        self._run_silence_tpl(textline)
        return {"vq_tempo": self.vq_tempo_1 + self.vq_silence}


    @validate_and_run
    def compute_vq_volume(self, textline):
        self._run_asterisk_tpl(textline)
        return {"vq_volume": self.vq_volume}


    @validate_and_run
    def compute_vq_censorship(self, textline):
        self._run_censorship_tpl(textline)
        return {"vq_censorship": self.vq_censorship}


    @validate_and_run
    def compute_vq_spelling(self, textline):
        self._run_spelling_tpl(textline)
        return {"vq_spelling": self.vq_spelling}


    @validate_and_run
    def compute_VQ(self, textline):
        self._run_wordbased_tpl(textline)
        self._run_rhythm_tpl(textline)
        self._run_emphasis_tpl(textline)
        self._run_silence_tpl(textline)
        self._run_asterisk_tpl(textline)
        self._run_censorship_tpl(textline)
        self._run_spelling_tpl(textline)
        self.vq_emphasis = self.vq_emphasis_1 + self.vq_emphasis_2
        self.vq_intst_emphasis = self.vq_intst_emphasis_1 + self.vq_intst_emphasis_2
        self.vq_tempo = self.vq_tempo_1 + self.vq_silence
        self.vq_intst_tempo = self.vq_intst_tempo_1 + self.vq_intst_silence
        self.vq = self.vq_pitch + self.vq_rhythm + self.vq_stress + self.vq_emphasis + self.vq_tempo + self.vq_volume + self.vq_censorship + self.vq_spelling
        return {"Voice Qualities": self.vq}


    @validate_and_run
    def compute_vs_alternants(self, textline):
        self._run_wordbased_tpl(textline)
        return {"vs_alternants": self.vs_alternants}

    @validate_and_run
    def compute_vs_differentiators(self, textline):
        self._run_wordbased_tpl(textline)
        self._run_asterisk_tpl(textline)
        return {"vs_differentiators": self.vs_differentiators_1 + self.vs_differentiators_asterisk}

    @validate_and_run
    def compute_VS(self, textline):
        self._run_wordbased_tpl(textline)
        self._run_asterisk_tpl(textline)
        self.vs_differentiators = self.vs_differentiators_1 + self.vs_differentiators_asterisk
        self.vs = self.vs_alternants + self.vs_differentiators
        return {"Vocalizations": self.vs}


    @validate_and_run
    def compute_tk_alphahaptics(self, textline):
        self._run_wordbased_tpl(textline)
        self._run_asterisk_tpl(textline)
        return { "tk_alphahaptics": self.tk_alphahaptics_1 + self.tk_alphahaptics_asterisk}


    @validate_and_run
    def compute_tk_bodilyemoticons(self, textline):
        self._run_emojicon_tpl(textline)
        return {"tk_tactile_emoticons": self.tk_bodilyemoticons}


    @validate_and_run
    def compute_tk_tactileemojis(self, textline):
        self._run_emojicon_tpl(textline)
        return {"tk_tactile_emojis": self.tk_tactileemojis}


    @validate_and_run
    def compute_TK(self, textline):
        self._run_wordbased_tpl(textline)
        self._run_asterisk_tpl(textline)
        self._run_emojicon_tpl(textline)
        self.tk_alphahaptics = self.tk_alphahaptics_1 + self.tk_alphahaptics_asterisk
        self.tk = self.tk_alphahaptics + self.tk_bodilyemoticons + self.tk_tactileemojis
        return { "Tactile Kinesics": self.tk}



    @validate_and_run
    def compute_vk_alphakinesics(self, textline):
        self._run_asterisk_tpl(textline)
        return {"vk_alphakinesics": self.vk_alphakinesics}


    @validate_and_run
    def compute_vk_bodilyemoticons(self, textline):
        self._run_emojicon_tpl(textline)
        return {"vk_bodily_emoticons": self.vk_bodilyemoticons}


    @validate_and_run
    def compute_vk_bodilyemojis(self, textline):
        self._run_emojicon_tpl(textline)
        return {"vk_bodily_emojis": self.vk_bodilyemojis}


    @validate_and_run
    def compute_VK(self, textline):
        self._run_asterisk_tpl(textline)
        self._run_emojicon_tpl(textline)
        self.vk = self.vk_alphakinesics + self.vk_bodilyemoticons + self.vk_bodilyemojis
        return { "Visual Kinesics": self.vk}



    @validate_and_run
    def compute_a_nonbodilyemoticons(self, textline):
        self._run_emojicon_tpl(textline)
        return {"a_nonbodily_emoticons": self.a_nonbodilyemoticons}


    @validate_and_run
    def compute_a_nonbodilyemojis(self, textline):
        self._run_emojicon_tpl(textline)
        return {"a_nonbodily_emojis": self.a_nonbodilyemojis}


    @validate_and_run
    def compute_a_formatting(self, textline):
        self._run_formatting_tpl(textline)
        return {"a_formatting": self.a_formatting}



    @validate_and_run
    def compute_ART(self, textline):
        self._run_formatting_tpl(textline)
        self._run_emojicon_tpl(textline)
        self.art = self.a_nonbodilyemoticons + self.a_nonbodilyemojis + self.a_formatting
        return { "Artifacts": self.art}



    @validate_and_run
    def compute_total_emoji_raw_count(self, textline):
        self._run_emojicon_tpl(textline)
        return {"Emoji_Count": self.tk_intst_tactileemojis + self.vk_intst_bodilyemojis + self.a_intst_nonbodilyemojis}


    @validate_and_run
    def compute_total_emoji_count(self, textline):
        self._run_emojicon_tpl(textline)
        return {"Emoji_Index": self.tk_tactileemojis + self.vk_bodilyemojis + self.a_nonbodilyemojis}

    @validate_and_run
    def compute_total_emoticon_count(self, textline):
        self._run_emojicon_tpl(textline)
        return {"Emoticon_Index": self.tk_bodilyemoticons + self.vk_bodilyemoticons + self.a_nonbodilyemoticons}




    @validate_and_run
    def all_modules(self, textline):
        self._run_wordbased_tpl(textline)
        self._run_emphasis_tpl(textline)
        self._run_silence_tpl(textline)
        self._run_asterisk_tpl(textline)
        self._run_censorship_tpl(textline)
        self._run_spelling_tpl(textline)
        self._run_rhythm_tpl(textline)

        self._run_asterisk_tpl(textline)
        self._run_emojicon_tpl(textline)

        self._run_formatting_tpl(textline)

        self.TPL_raw_count = self.vq_stress + self.vq_pitch + self.vq_tempo_1 + self.vq_emphasis_1 + self.vq_emphasis_2 + self.vq_volume  + self.vq_rhythm + self.vq_censorship + self.vq_spelling + self.vq_silence + \
        self.vs_alternants + self.vs_differentiators_1 + self.vs_differentiators_asterisk + \
        self.tk_alphahaptics_1  + self.tk_alphahaptics_asterisk + self.tk_tactileemojis + self.tk_bodilyemoticons + \
        self.vk_alphakinesics + self.vk_bodilyemojis + self.vk_bodilyemoticons + \
        self.a_emoji_symbol + self.a_nonbodilyemojis + self.a_nonbodilyemoticons + self.a_formatting

        self.vq_emphasis = self.vq_emphasis_1 + self.vq_emphasis_2
        self.vs_differentiators = self.vs_differentiators_asterisk + self.vs_differentiators_1
        self.tk_alphahaptics = self.tk_alphahaptics_1  + self.tk_alphahaptics_asterisk
        self.a_nonbodilyemoticons = self.a_nonbodilyemoticons + self.a_emoji_symbol
        self.vq_tempo = self.vq_tempo_1 + self.vq_silence
        self.total_emoticon_count = self.tk_bodilyemoticons + self.vk_bodilyemoticons + self.a_nonbodilyemoticons
        self.total_emoji_count = self.tk_tactileemojis + self.vk_bodilyemojis + self.a_nonbodilyemojis
        self.total_emoji_raw_count = self.tk_intst_tactileemojis + self.vk_intst_bodilyemojis + self.a_intst_nonbodilyemojis



        return {
        "vq_pitch": self.vq_pitch, 
        "vq_rhythm": self.vq_rhythm, 
        "vq_stress": self.vq_stress, 
        "vq_emphasis": self.vq_emphasis, 
        "vq_tempo": self.vq_tempo, 
        "vq_volume": self.vq_volume, 
        "vq_censorship": self.vq_censorship, 
        "vq_spelling": self.vq_spelling, 
        "vs_alternants": self.vs_alternants, 
        "vs_differentiators": self.vs_differentiators, 
        "tk_tactile_alphahaptics": self.tk_alphahaptics, 
        "tk_tactile_bodilyemoticons": self.tk_bodilyemoticons, 
        "tk_tactile_tactileemojis": self.tk_tactileemojis, 
        "vk_alphakinesics": self.vk_alphakinesics, 
        "vk_bodily_emoticons": self.vk_bodilyemoticons, 
        "vk_bodily_emojis": self.vk_bodilyemojis, 
        "a_formatting": self.a_formatting, 
        "a_nonbodily_emoticons": self.a_nonbodilyemoticons, 
        "a_nonbodily_emojis": self.a_nonbodilyemojis, 
        "Emoji_Count": self.total_emoji_raw_count, 
        "Emoji_Index": self.total_emoji_count, 
        "Emoticon_Index": self.total_emoticon_count, 
        "TPL_Index": self.TPL_raw_count
    }




    # def run(self, textline):
    #     try:
    #         if type(textline) == str and len(textline.strip()) > 0:                                        
    #             res = self.all_modules(textline)
    #             return res
    #         else:
    #             textline = str(textline) + ' '
    #             res = self.all_modules(textline)
    #             return res        
    #     except Exception:
    #         print(traceback.print_exc())









