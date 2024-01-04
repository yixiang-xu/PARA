##### function: Detect_Formatting (detection of formatting TPL)

import re
def Detect_Formatting(textlines):

    if str(type(textlines))!= "<class 'list'>":
        print("the type of the textline should be list")
        return
        
    pattern1 = pattern2 = pattern3 = pattern4 = pattern5 =[]

    point = ["•","◦", "∙","«","»","‣","☑","✔", "✅","✓","☑","✔","𐄂","⍻","⑇",
    "☑", "▲","△","▴","▵","▷","▹","►","▻","▼","▽","▾","▿","◁","☛","☞","✦", 
    "✧","✵","✶","✷","✸","✹", "✺","☝","❂","✴","▶","◀","«","»","[check]","step"]
    point = list(set(point))

    count_point_begin = []
    count_point_middle = []
    count_point_end = []
    list_pattern = 0

    # possib 1. search for: point (in the point list) + content
                        #   point + content
                        #   point + content
    # first check if is the list structure
    raw_textlines  = textlines
    textlines = [text.lower() for text in textlines]
    textlines = " ".join(textlines)
    for k in point:
        pattern = re.compile(r"("+k+"([a-zA-Z1-9 ]+)[.,;]*){3,}")
        n_format = len(pattern.findall(textlines))

    # possib 2. search for: 1 + content 2 + content 3 + content
    pattern = re.compile(r"([1-9][.,:) ][ ]*[a-zA-Z ]+[.; ]*)")
    mt_format = pattern.finditer(textlines)
    mt_format = [w.group() for w in mt_format]
    if len(mt_format)>=3:
        i = 0
        while i+2 < len(mt_format):
            if mt_format[i][0] =="1" and mt_format[i+1][0]=="2" and mt_format[i+2][0] == "3":
                n_format = n_format + 1
                i = i + 3
            else:
                i = i + 1

    # possib 3. search for: a + content b + content c + content
    pattern = re.compile(r"([a-c][.,:) ][ ]*[a-zA-Z ]+[.; ]*)")
    mt_format = pattern.finditer(textlines)
    mt_format = [w.group() for w in mt_format]
    if len(mt_format)>=3:
        i = 0 
        while i+2 < len(mt_format):
            if mt_format[i][0] =="a" and mt_format[i+1][0] =="b" and mt_format[i+2][0] == "c":
                n_format = n_format + 1
                i = i + 3
            else:
                i = i + 1
    
    # possible 4. more than two line breaks
    if len(raw_textlines)>=3:
        count = 0
        for item in raw_textlines:
            item_len = len(item)
            item_en = len(re.findall(r"[a-z-A-Z]",item))
            if item_len>1 and item_en>1:
                count = count + 1
        if count >=3:
            n_format = n_format + 1

    return n_format


