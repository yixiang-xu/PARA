from setuptools import setup, find_packages
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read(),  # Long description read from the readme file
        
setup(
    name='para_paralanguage_classifier',
    version='0.1',  # Your package's version
    author='Yixiang Xu',  # Your name or your organization's name
    author_email='yixiang-xu@berkeley.edu',  # Your email or your organization's email
    description='''The Textual Paralanguage Classifier, called PARA, 
    is a computerized text analysis software for detecting nonverbal communication cues in text. 
    PARA is designed for researchers and practitioners who are interested in text analytics to detect language beyond what is said verbally, 
    to how it is said nonverbally. Analogous to the identification of ``properties of speech'' such as nouns, verbs, 
    or prepositions in verbal content, PARA categorizes the ``properties of nonverbal speech'' denoted in text. 
    This tool is particularly well suited for processing social media data, 
    as this form of text often includes informal communication such as emojis. 
    PARA will help you capture the auditory, visual, and tactile elements of nonverbal text speech which may reveal thoughts, feelings, personality, motivations, and behaviors.''',  # A short description
    long_description=long_description,
    long_description_content_type='text/markdown',  # Type of the long description, usually markdown or plain text
    url='https://textualparalanguage.com/',  # Link to your package's GitHub repo or website
    packages=find_packages(),  # Automatically find all packages and subpackages
    install_requires=[
        'numpy==1.24.4',  # Replace with the minimum version your package requires
        'pandas==2.0.3',
        'regex==2022.1.18',
        'nltk==3.7',
        'openpyxl==3.1.2',
    ],
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',  
    'Operating System :: OS Independent',
],
    package_data={'para_paralanguage_classifier': ['TPL_support_files/*']},
    python_requires='>=3.7',  # Specify the minimum version of Python required
    include_package_data=True,  # Whether to include non-code files specified in MANIFEST.in
    keywords='keyword1 keyword2 keyword3',
    project_urls={
        'Source': 'https://github.com/yixiang-xu/PARA',
        'Paper': 'https://journals.sagepub.com/doi/full/10.1177/00222437221116058'
    },
)

