from setuptools import setup

setup(
    name='jf_tokenize_package',
    version='1.0.2',
    license='MIT',
    author="Julien Flandre",
    author_email='julien.flandre@gmail.com',
    description='A simple tokenizer function for NLP',
    long_description='This tokenizer function turns text into lowercase word \
                      tokens, removes English stopwords, lemmatize the tokens \
                      and replaces URLs with a placeholder.',
    long_description_content_type='text/x-rst',
    packages=['jf_tokenize_package'],
    url='https://github.com/Granju/tokenize-package',
    keywords='tokenizer function'

)
