##### main function: Detect_Emojicon_TPL (detection of TPL elements that are emoji / emoticon based, including TK tactile emoji, tactile emoticon, VK bodily emoji, bodily emoticon, Artifact nonbodily emoji, nonbodily emoticon)
from .check_emojis import check_emojis
from .check_emoticon import check_emoticon
def Detect_Emojicon_TPL(textline, key_emoji, key_emoticon, emoticon_hier_tk, emoticon_hier_vk, emoticon_hier_a):

    if str(type(textline))!= "<class 'str'>":
        print("the type of the textline should be string")
        return
    
    if str(type(key_emoji))!= "<class 'dict'>":
        print("the type of the key_emoji should be dictionary")
        return

    if str(type(key_emoticon))!= "<class 'dict'>":
        print("the type of the key_emoticon should be dictionary")
        return
    
    tk_emoji = check_emojis(textline, key_emoji,"tk")
    vk_emoji = check_emojis(textline, key_emoji,"vk")
    a_emoji = check_emojis(textline, key_emoji,"a")

    tk_emoji_count = tk_emoji[0]
    vk_emoji_count = vk_emoji[0]
    a_emoji_count = a_emoji[0]

    tk_emoji_intst = tk_emoji[1]
    vk_emoji_intst = vk_emoji[1]
    a_emoji_intst = a_emoji[1]


    emoticon_hier = {'tk':emoticon_hier_tk, 'vk':emoticon_hier_vk, 'a':emoticon_hier_a}
    ### pre-processing input text ###
    textline = textline.split()
    wordlist = []
    for w in textline:
        if w.startswith("#") or w.startswith("http:") or w.startswith("https:") or w.startswith("@") or w.startswith("RT"):
            wordlist = wordlist + ["tplandrea"]
        else:
            wordlist = wordlist + [w]

    textline = " ".join(wordlist) + "\n"
    raw_textline = textline


    tk_emoticon = check_emoticon(textline, emoticon_hier,"tk")
    vk_emoticon = check_emoticon(textline, emoticon_hier,"vk")
    a_emoticon = check_emoticon(textline, emoticon_hier,"a")

    tk_emoticon_count = tk_emoticon[0]
    vk_emoticon_count = vk_emoticon[0]
    a_emoticon_count = a_emoticon[0]

    tk_emoticon_intst = tk_emoticon[1]
    vk_emoticon_intst = vk_emoticon[1]
    a_emoticon_intst = a_emoticon[1]



    return tk_emoji_count,vk_emoji_count,a_emoji_count,tk_emoticon_count,vk_emoticon_count,a_emoticon_count,tk_emoji_intst,vk_emoji_intst,a_emoji_intst,tk_emoticon_intst,vk_emoticon_intst,a_emoticon_intst




