# PARA Python Package

## Introduction

**PARA** (Textual Paralanguage Classifier) is a computerized text analysis software designed to detect nonverbal communication cues in text. It is ideal for researchers and practitioners in text analytics, aimed at uncovering the "properties of nonverbal speech" denoted in text, particularly useful in social media data analysis.

## What is TPL?

TPL, or Textual Paralanguage, represents written manifestations of nonverbal audible, tactile, and visual elements in text. These can be expressed through words, symbols, images, punctuation, demarcations, etc. PARA categorizes TPL into five main categories: voice qualities (VQ), vocalizations (VS), tactile kinesics (TK), visual kinesics (VK), and artifacts (A). Unlike traditional text analytics, PARA focuses on the extratextual features of written communication.

![Description](https://static.wixstatic.com/media/62e0e2_24d79b8cc93e4e689d77b838535166d1~mv2.jpg/v1/fill/w_1336,h_944,al_c,q_85,enc_auto/Table%201.jpg)


## Usage and Citation

When using PARA, please cite as follows:
> Luangrath, Andrea W., Yixiang Xu, and Tong Wang (2023), “Paralanguage Classifier (PARA): An Algorithm for Automatic Coding of Paralinguistic Nonverbal Parts of Speech in Text,” Journal of Marketing Research, 60 (2), 388-408.


## Functions and Outputs

### Overview
The PARA package offers a range of functions designed to extract various nonverbal features from text. These functions are categorized into subordinate level nonverbal features and category level nonverbal features. Additionally, the package provides functions to compute aggregate variables such as emoji and emoticon counts.
![Description](https://static.wixstatic.com/media/62e0e2_7da7b5eab30e45cab3b4802fc416dd06~mv2.jpg/v1/fill/w_2166,h_862,al_c,q_85,enc_auto/Table%202.jpg)


### Sample Code 
We will distribute this package through PyPI soon for easier installation soon. For now, you can install the PARA Python package using the following commands:

1. **Download and Build the Package:**
   First, clone the repository from GitHub and build the package using `python setup.py bdist_wheel`:
   ```terminal
   git clone https://github.com/yixiang-xu/PARA.git
   cd PARA
   mv build/lib/para_paralanguage_classifier .
   python setup.py bdist_wheel
   ```
2. **Install the Package:**
	After building, install the package with pip:  
	```terminal
	pip install dist/para_paralanguage_classifier-0.1-py3-none-any.whl
	``` 

You can use the following sample code to extract your desired nonverbal features from a text line.

```python
from para_paralanguage_classifier import para_output
PARA = para_output()

textline = 'You Define'
# Voice Quality functions
vq_pitch = PARA.compute_vq_pitch(textline)
vq_rhythm = PARA.compute_vq_rhythm(textline)
vq_stress = PARA.compute_vq_stress(textline)
vq_emphasis = PARA.compute_vq_emphasis(textline)
vq_tempo = PARA.compute_vq_tempo(textline)
vq_volume = PARA.compute_vq_volume(textline)
vq_censorship = PARA.compute_vq_censorship(textline)
vq_spelling = PARA.compute_vq_spelling(textline)
vq_overall = PARA.compute_VQ(textline)

# Vocalizations functions
vs_alternants = PARA.compute_vs_alternants(textline)
vs_differentiators = PARA.compute_vs_differentiators(textline)
vs_overall = PARA.compute_VS(textline)

# Tactile Kinesics functions
tk_alphahaptics = PARA.compute_tk_alphahaptics(textline)
tk_bodilyemoticons = PARA.compute_tk_bodilyemoticons(textline)
tk_tactileemojis = PARA.compute_tk_tactileemojis(textline)
tk_overall = PARA.compute_TK(textline)

# Visual Kinesics functions
vk_alphakinesics = PARA.compute_vk_alphakinesics(textline)
vk_bodilyemoticons = PARA.compute_vk_bodilyemoticons(textline)
vk_bodilyemojis = PARA.compute_vk_bodilyemojis(textline)
vk_overall = PARA.compute_VK(textline)

# Artifacts functions
a_nonbodilyemoticons = PARA.compute_a_nonbodilyemoticons(textline)
a_nonbodilyemojis = PARA.compute_a_nonbodilyemojis(textline)
a_formatting = PARA.compute_a_formatting(textline)
art_overall = PARA.compute_ART(textline)

# Aggregate Variables 
emoji_count = PARA.compute_total_emoji_raw_count(textline) 
emoji_index = PARA.compute_total_emoji_count(textline) 
emoticon_index = PARA.compute_total_emoticon_count(textline) 

# Example of using all modules for a comprehensive analysis
all_results = PARA.all_modules(textline)
```


## Code Structure

The following code modules are the building block wrappers for output the nonverbal features. 

- `TPL_Int_Score.py`: Compiles all PARA modules.
- `test.py`: Test script for `TPL_Int_Score.py`, available in two versions: with and without multiprocessing.
- `Detect_Wordbased_TPL`: Folder containing word/phrase based TPL element detection (VQ stress, pitch, tempo, emphasis, etc.).
- `Detect_Silence`: Module for detecting the repetition of silence symbols.
- `Detect_Emphasis`: Module for detecting word/phrase repetition and punctuation repetition.
- `Detect_Spelling`: Module for detecting words connected by symbols (e.g., s-l-o-w).
- `Detect_Rhythm`: Module for detecting word-symbol alternations.
- `Detect_Censorship`: Module for detecting censorship.
- `Detect_Asterisk_TPL`: Folder for asterisk pattern TPL elements detection (VQ volume, VK alphakinesics, etc.).
- `Detect_Emojicon_TPL`: Folder for emoji/emoticon based TPL elements detection.
- `Detect_Formatting`: Module for detecting formatting.
