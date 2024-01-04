
############### Apply function --  Detect_Wordbased_TPL ###############

###### 8v 
import sys 
import os
dir = "/Volumes/Seagate/Research/PARA/PARA"

sys.path.append(dir)
os.chdir('/Volumes/Seagate/Research/PARA/PARA')

from nltk.corpus import brown

brown_dic_ls = set(brown.words())


from TPL_Int_Score import TPL_Int_Score
from TPL_Int_Score import Prep
PARA = TPL_Int_Score("TPL_support_files/Keyword List_Without Symbol.xlsx", "TPL_support_files/Excluded Acronyms.xlsx","TPL_support_files/Keyword List_With Symbol.xlsx", "TPL_support_files/cursing_lexicon.txt", \
	"TPL_support_files/emoticon_a.txt", "TPL_support_files/emoticon_vk.txt", "TPL_support_files/emoticon_tk.txt","TPL_support_files/Emoji Dictionary.xlsx", brown_dic_ls)

#PARA.run('this is greatttt')
# prep = Prep("TPL_support_files/Keyword List_Without Symbol.xlsx", "TPL_support_files/Excluded Acronyms.xlsx","TPL_support_files/Keyword List_With Symbol.xlsx", "TPL_support_files/cursing_lexicon.txt", \
# 	"TPL_support_files/emoticon_a.txt", "TPL_support_files/emoticon_vk.txt", "TPL_support_files/emoticon_tk.txt","TPL_support_files/Emoji Dictionary.xlsx", brown_dic_ls)

import pandas as pd 
data = pd.read_excel('/Volumes/Seagate/Research/PARA/PARA/test-sample/Classifier Test.xlsx')
import time
start = time.time()
for i in range(data.shape[0]):
	temp = PARA.run(data['TEXT'].iloc[i])
	print(i)

duration = time.time() - start



###### 8v + concurrent
import sys 
import concurrent.futures
import os
dir = "/Volumes/Seagate/Research/PARA/PARA"

sys.path.append(dir)
os.chdir('/Volumes/Seagate/Research/PARA/PARA')

from nltk.corpus import brown

brown_dic_ls = set(brown.words())


from TPL_Int_Score import TPL_Int_Score
from TPL_Int_Score import Prep
PARA = TPL_Int_Score("TPL_support_files/Keyword List_Without Symbol.xlsx", "TPL_support_files/Excluded Acronyms.xlsx","TPL_support_files/Keyword List_With Symbol.xlsx", "TPL_support_files/cursing_lexicon.txt", \
	"TPL_support_files/emoticon_a.txt", "TPL_support_files/emoticon_vk.txt", "TPL_support_files/emoticon_tk.txt","TPL_support_files/Emoji Dictionary.xlsx", brown_dic_ls)

#PARA.run('this is greatttt')
# prep = Prep("TPL_support_files/Keyword List_Without Symbol.xlsx", "TPL_support_files/Excluded Acronyms.xlsx","TPL_support_files/Keyword List_With Symbol.xlsx", "TPL_support_files/cursing_lexicon.txt", \
# 	"TPL_support_files/emoticon_a.txt", "TPL_support_files/emoticon_vk.txt", "TPL_support_files/emoticon_tk.txt","TPL_support_files/Emoji Dictionary.xlsx", brown_dic_ls)

import pandas as pd 
data = pd.read_csv('/Volumes/Seagate/Research/PARA/PARA/test-sample/Classifier Test.xlsx')
import time


temp = []
results=[]

start = time.time()
with concurrent.futures.ProcessPoolExecutor() as executor:
    for i in executor.map(PARA.run,data['TEXT']):
        results.append(i)


for index,result in enumerate(results):
    temp.append(result)


duration = time.time() - start


###### 7v 
import sys 
import os
dir = "/Volumes/Seagate/Research/PARA/PARA"

sys.path.append(dir)
os.chdir('/Volumes/Seagate/Research/PARA/PARA')

from nltk.corpus import brown

brown_dic_ls = set(brown.words())


from TPL_Int_Score import TPL_Int_Score

import pandas as pd 
data = pd.read_csv('/Volumes/Seagate/Research/PARA/PARA/test-sample/Classifier Test.xlsx')
import time
start = time.time()
for i in range(data.shape[0]):
	temp = TPL_Int_Score(dir, data['TEXT'].iloc[i], brown_dic)
	print(i)

duration = time.time() - start


temp = []
results=[]

start = time.time()

def do(textline):
    return(TPL_Int_Score(dir, textline, brown_dic))

with concurrent.futures.ProcessPoolExecutor() as executor:
    for i in executor.map(do,data['TEXT']):
        results.append(i)


for index,result in enumerate(results):
    temp.append(result)


duration = time.time() - start










textline = "THIS IS GREATTT !!!!"
textline = "Yayyyy! THIS IS GREAT"
textline = "this is cute ;P ;p"  # update point 2
textline = "this is cute ayy yoink" # update point 3
textline = "*this is cute*" # update point 5
textline = "::this is cute::" # update point 5
textline = "this is cute.. such a cute boy" # update point 6
textline = "this is cute.." # update point 6
textline = "this is so Greaaaaatttttttt news" # update point 7
textline = "finally, Best. Day. Ever!!!" # update point 8
textline = "I finish shoutout shoutoutoutout" # update point 10
textline = "I finish shoutout" # update point 10
textline = "*high five back*" # update point 11
textline = "this is ____ secret " # update point 12

TPL_Int_Score(dir, textline, brown_dic)




data = pd.read_csv('/Volumes/Seagate/Research/PARA/PARA/test-sample/Classifier Test.xlsx')
import time
start = time.time()
for i in range(data.shape[0]):
	temp = Detect_Emojicon_TPL(data['TEXT'].iloc[i], key_emoji, key_emoticon)


duration = time.time() - start