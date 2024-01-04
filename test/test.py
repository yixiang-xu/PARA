import os
dir = "."
os.chdir('.')

from para_paralanguage_classifier import para_output
PARA = para_output()



##### For Individual Modules 
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


PARA.compute_vq_pitch(textline) 
PARA.compute_vq_rhythm(textline) 
PARA.compute_vq_stress(textline) 
PARA.compute_vq_emphasis(textline) 
PARA.compute_vq_tempo(textline) 
PARA.compute_vq_volume(textline) 
PARA.compute_vq_censorship(textline) 
PARA.compute_vq_spelling(textline) 
PARA.compute_VQ(textline) 
PARA.compute_vs_alternants(textline) 
PARA.compute_vs_differentiators(textline) 
PARA.compute_VS(textline) 
PARA.compute_tk_alphahaptics(textline) 
PARA.compute_tk_bodilyemoticons(textline) 
PARA.compute_tk_tactileemojis(textline) 
PARA.compute_TK(textline) 
PARA.compute_vk_alphakinesics(textline) 
PARA.compute_vk_bodilyemoticons(textline) 
PARA.compute_vk_bodilyemojis(textline) 
PARA.compute_VK(textline) 
PARA.compute_a_nonbodilyemoticons(textline) 
PARA.compute_a_nonbodilyemojis(textline) 
PARA.compute_a_formatting(textline) 
PARA.compute_ART(textline) 
PARA.compute_total_emoji_raw_count(textline) 
PARA.compute_total_emoji_count(textline) 
PARA.compute_total_emoticon_count(textline) 


PARA.all_modules(textline)







##### Test A Loop 

import pandas as pd 
data = pd.read_excel('./test/Classifier Test.xlsx')
import time
start = time.time()
for i in range(data.shape[0]):
	temp = PARA.all_modules(data['TEXT'].iloc[i])
	print(i)

duration = time.time() - start



###### concurrent
temp = []
results=[]

start = time.time()
with concurrent.futures.ProcessPoolExecutor() as executor:
    for i in executor.map(PARA.run,data['TEXT']):
        results.append(i)


for index,result in enumerate(results):
    temp.append(result)


duration = time.time() - start











