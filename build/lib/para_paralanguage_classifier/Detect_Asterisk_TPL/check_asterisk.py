##### supporting function: check_asterisk (detect asterisk TPL pattern, including following symbols {}, [], (),<>, *, ",',::,\\,//, --, ♫ e.g. *great*

import re

def check_asterisk(textline, key_word_dic, type):
     
    ######### pre-processed the key word list #############
    # de-capitalization the key words
    if type == "vq":
        key_word_dic = key_word_dic["vq"]
    elif type == "vs":
        key_word_dic = key_word_dic["vs"]
    elif type == "tk":
        key_word_dic = key_word_dic["tk"]
    elif type == "vk":
        non_key_word_dic = key_word_dic["nvk"]
        key_word_dic = key_word_dic["vk"]
    elif type == "a":
        non_key_word_dic = key_word_dic["na"]
        key_word_dic = key_word_dic["a"]

    key_word_dic = [w.lower() for w in key_word_dic]

    if type == "vk" or type == "a":
        non_key_word_dic = [w.lower() for w in non_key_word_dic]


    asterisk_count = 0

    ######### detecting asterisk pattern by symbol #############
    # {}
    r = re.compile(r"(\{[a-zA-Z0-9 .,-]+\})\1*")
    case = r.findall(textline)
    if len(case)!=0:
        for c in case:
            # tease out the symbols 
            word = [w for w in re.split(r"[\{\} ]",c) if w!=""]
            if type == "a": # * for just vk
                na_count = len([w for w in word if w.lower() in non_key_word_dic])
                nemoji_count = len(re.findall(r"emoji",c))
                if na_count == 0 and nemoji_count!=0:
                    asterisk_count = asterisk_count + 1
            else:
                for w in word:
                    if w.lower() in key_word_dic:
                        asterisk_count = asterisk_count + 1
                        break
                key_phrase = [w for w in key_word_dic if " " in w] # check if a phrase match
                match_phrase = [len(re.findall(w,c)) for w in key_phrase]
                if sum(match_phrase)>0:
                    asterisk_count = asterisk_count + 1



    # []
    r = re.compile(r"(\[[a-zA-Z0-9 .,-]+\])\1*")
    case = r.findall(textline)
    if len(case)!=0:
        for c in case:
            # tease out the symbols 
            word = [w for w in re.split(r"[\[\] ]",c) if w!=""]
            if type == "a": # * for just vk
                na_count = len([w for w in word if w.lower() in non_key_word_dic])
                nemoji_count = len(re.findall(r"emoji",c))
                if na_count == 0 and nemoji_count!=0:
                    asterisk_count = asterisk_count + 1
            else:
                for w in word:
                    if w.lower() in key_word_dic:
                        asterisk_count = asterisk_count + 1
                        break
                key_phrase = [w for w in key_word_dic if " " in w] # check if a phrase match
                match_phrase = [len(re.findall(w,c)) for w in key_phrase]
                if sum(match_phrase)>0:
                    asterisk_count = asterisk_count + 1

    # ()
    r = re.compile(r"(\([a-zA-Z0-9 .,-]+\))\1*")
    case = r.findall(textline)
    if len(case)!=0:
        for c in case:
            # tease out the symbols 
            word = [w for w in re.split(r"[\(\) ]",c) if w!=""]
            if type == "a": # * for just vk
                na_count = len([w for w in word if w.lower() in non_key_word_dic])
                nemoji_count = len(re.findall(r"emoji",c))
                if na_count == 0 and nemoji_count!=0:
                    asterisk_count = asterisk_count + 1
            else:
                for w in word: # check if there is a word based match
                    if w.lower() in key_word_dic:
                        asterisk_count = asterisk_count + 1
                        break
                key_phrase = [w for w in key_word_dic if " " in w] # check if a phrase match
                match_phrase = [len(re.findall(w,c)) for w in key_phrase]
                if sum(match_phrase)>0:
                    asterisk_count = asterisk_count + 1

    # <>
    r = re.compile(r"(\<[a-zA-Z0-9 .,-]+\>)\1*")
    case = r.findall(textline)
    if len(case)!=0:
        for c in case:
            # tease out the symbols 
            word = [w for w in re.split(r"[\<\> ]",c) if w!=""]
            if type == "a": # * for just a
                na_count = len([w for w in word if w.lower() in non_key_word_dic])
                nemoji_count = len(re.findall(r"emoji",c))
                if na_count == 0 and nemoji_count!=0:
                    asterisk_count = asterisk_count + 1
            else:
                for w in word:
                    if w.lower() in key_word_dic:
                        asterisk_count = asterisk_count + 1
                        break
                key_phrase = [w for w in key_word_dic if " " in w] # check if a phrase match
                match_phrase = [len(re.findall(w,c)) for w in key_phrase]
                if sum(match_phrase)>0:
                    asterisk_count = asterisk_count + 1

    # *
    r = re.compile(r"(\*[a-zA-Z0-9 .,-]+\*)\1*")
    case = r.findall(re.sub(r"\*\*|\*",r"**",textline))
    if len(case)!=0:
        for c in case:
            # tease out the symbols 
            word = [w for w in re.split(r"[\* ]",c) if w!=""]
            if type == "vk": # * for just vk
                nvk_count = len([w for w in word if w.lower() in non_key_word_dic]) 
                join_word = [" ".join(word)]
                nvk_count = nvk_count + len([w for w in join_word if w in non_key_word_dic])
                nemoji_count = len(re.findall(r"emoji",c))
                if nvk_count == 0 and nemoji_count==0 and len(word)!=0:
                    asterisk_count = asterisk_count + 1
            elif type == "a": # * for just vk
                na_count = len([w for w in word if w.lower() in non_key_word_dic])
                nemoji_count = len(re.findall(r"emoji",c))
                if na_count == 0 and nemoji_count!=0:
                    asterisk_count = asterisk_count + 1
            else:
                for w in word:
                    if w.lower() in key_word_dic:
                        asterisk_count = asterisk_count + 1
                        break
                key_phrase = [w for w in key_word_dic if " " in w] # check if a phrase match
                match_phrase = [len(re.findall(w,c)) for w in key_phrase]
                if sum(match_phrase)>0:
                    asterisk_count = asterisk_count + 1


    # capture: ::whisper
    r = re.compile(r"(\:\:[a-zA-Z0-9 .,-]+\:\:)\1*")
    case = r.findall(re.sub(r"\:\:",r"::::",textline))
    if len(case)!=0:
        for c in case:
            # tease out the symbols
            word = [w for w in re.split(r"[\: ]",c) if w!=""]
            if type == "vk": # * for just vk
                nvk_count = len([w for w in word if w.lower() in non_key_word_dic])
                join_word = [" ".join(word)]
                nvk_count = nvk_count + len([w for w in join_word if w in non_key_word_dic])
                nemoji_count = len(re.findall(r"emoji",c))
                if nvk_count == 0 and nemoji_count==0 and len(word)!=0:
                    asterisk_count = asterisk_count + 1
                elif type == "a": # * for just vk
                    na_count = len([w for w in word if w.lower() in non_key_word_dic])
                    nemoji_count = len(re.findall(r"emoji",c))
                    if na_count == 0 and nemoji_count!=0:
                        asterisk_count = asterisk_count + 1
                else:
                    for w in word:
                        if w.lower() in key_word_dic:
                            asterisk_count = asterisk_count + 1
                            break
                    key_phrase = [w for w in key_word_dic if " " in w] # check if a phrase match
                    match_phrase = [len(re.findall(w,c)) for w in key_phrase]
                    if sum(match_phrase)>0:
                        asterisk_count = asterisk_count + 1


    # - -
    r = re.compile(r"(\-[a-zA-Z0-9 .,-]+\-)\1*")
    case = r.findall(re.sub(r"\-\-|\-",r"--",textline))
    if len(case)!=0:
        for c in case:
            # tease out the symbols
            word = [w for w in re.split(r"[\- ]",c) if w!=""]
            if type == "a": # * for just vk
                na_count = len([w for w in word if w.lower() in non_key_word_dic])
                nemoji_count = len(re.findall(r"emoji",c))
                if na_count == 0 and nemoji_count!=0:
                    asterisk_count = asterisk_count + 1
            else:
                for w in word:
                    if w.lower() in key_word_dic:
                        asterisk_count = asterisk_count + 1
                        break
                key_phrase = [w for w in key_word_dic if " " in w] # check if a phrase match
                match_phrase = [len(re.findall(w,c)) for w in key_phrase]
                if sum(match_phrase)>0:
                    asterisk_count = asterisk_count + 1


    # / /
    r = re.compile(r"(\/[a-zA-Z0-9 .,-]+\/)\1*")
    case = r.findall(re.sub(r"\/\/|\/",r"//",textline))
    if len(case)!=0:
        for c in case:
            # tease out the symbols
            word = [w for w in re.split(r"[\/ ]",c) if w!=""]
            if type == "a": # * for just vk
                na_count = len([w for w in word if w.lower() in non_key_word_dic])
                nemoji_count = len(re.findall(r"emoji",c))
                if na_count == 0 and nemoji_count!=0:
                    asterisk_count = asterisk_count + 1
            else:
                for w in word:
                    if w.lower() in key_word_dic:
                        asterisk_count = asterisk_count + 1
                        break
                key_phrase = [w for w in key_word_dic if " " in w] # check if a phrase match
                match_phrase = [len(re.findall(w,c)) for w in key_phrase]
                if sum(match_phrase)>0:
                    asterisk_count = asterisk_count + 1

    # \ \ #
    r = re.compile(r"(\\[a-zA-Z0-9 .,-]+\\)\1*")
    case = r.findall(re.sub(r"\\\\|\\",r"\\",textline))
    if len(case)!=0:
        for c in case:
            # tease out the symbols
            word = [w for w in re.split(r"[\\ ]",c) if w!=""]
            if type == "a": # * for just vk
                na_count = len([w for w in word if w.lower() in non_key_word_dic])
                nemoji_count = len(re.findall(r"emoji",c))
                if na_count == 0 and nemoji_count!=0:
                    asterisk_count = asterisk_count + 1
            else:
                for w in word:
                    if w.lower() in key_word_dic:
                        asterisk_count = asterisk_count + 1
                        break
                key_phrase = [w for w in key_word_dic if " " in w] # check if a phrase match
                match_phrase = [len(re.findall(w,c)) for w in key_phrase]
                if sum(match_phrase)>0:
                    asterisk_count = asterisk_count + 1


    # capture: ♫
    if type == "vq":
        r = re.compile(r"(♫[a-zA-Z0-9 .,]+♫)\1*")
        case = r.findall(re.sub(r"♫♫|♫",r"♫♫",textline))
        if len(case)!=0:
            asterisk_count = asterisk_count + 1



    # capture: 🎶
    if type == "vq":
        r = re.compile(r"(🎶[a-zA-Z0-9 .,]+🎶)\1*")
        case = r.findall(re.sub(r"🎶🎶|🎶",r"🎶🎶",textline))
        if len(case)!=0:
            asterisk_count = asterisk_count + 1

    
    return asterisk_count









#####################
# backup 

    # capture: " "
    r = re.compile(r'(\"[a-zA-Z0-9 .,-]+\")\1*')
    case = r.findall(re.sub(r'\"\"|\"',r'""',textline))
    if len(case)!=0:
        for c in case:
            # tease out the symbols
            word = [w for w in re.split(r'[\" ]',c) if w!=""]
            if type == "a": # * for just vk
                na_count = len([w for w in word if w.lower() in non_key_word_dic])
                nemoji_count = len(re.findall(r"emoji",c))
                if na_count == 0 and nemoji_count!=0:
                    asterisk_count = asterisk_count + 1
            else:
                for w in word:
                    if w.lower() in key_word_dic:
                        asterisk_count = asterisk_count + 1
                        break
                key_phrase = [w for w in key_word_dic if " " in w] # check if a phrase match
                match_phrase = [len(re.findall(w,c)) for w in key_phrase]
                if sum(match_phrase)>0:
                    asterisk_count = asterisk_count + 1



    # capture: ' '
    r = re.compile(r"(\'[a-zA-Z0-9 .,-]+\')\1*")
    case = r.findall(re.sub(r"\'\'|\'",r"''",textline))
    if len(case)!=0:
        for c in case:
            # tease out the symbols
            word = [w for w in re.split(r"[\' ]",c) if w!=""]
            if type == "a": # * for just vk
                na_count = len([w for w in word if w.lower() in non_key_word_dic])
                nemoji_count = len(re.findall(r"emoji",c))
                if na_count == 0 and nemoji_count!=0:
                    asterisk_count = asterisk_count + 1
            else:
                for w in word:
                    if w.lower() in key_word_dic:
                        asterisk_count = asterisk_count + 1
                        break
                key_phrase = [w for w in key_word_dic if " " in w] # check if a phrase match
                match_phrase = [len(re.findall(w,c)) for w in key_phrase]
                if sum(match_phrase)>0:
                    asterisk_count = asterisk_count + 1


