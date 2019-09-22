import re
from heapq import nlargest
import bs4 as bs  
import urllib.request
import spacy 
nlp = spacy.load('en_core_web_lg')
from spacy.lang.en.stop_words import STOP_WORDS
stopwords = list(STOP_WORDS)
from string import punctuation

# web scraping
def text_from_url(URL):
    article=urllib.request.urlopen(URL)
    parsed_article=bs.BeautifulSoup(article,'lxml')
    paragraphs=parsed_article.find_all('p')
    article_text=" "
    for p in paragraphs:
        article_text += p.text
    return(str(article_text))
    
# Cleaning the source text
def clean_text(text):
    text=re.sub(r'\[[0-9]*\]',' ',text)               
    text=re.sub(r'\s+',' ',text)
    text_2=text
    text_2=re.sub('[^a-zA-Z]',' ',text)        
    text_2=re.sub(r'\s+',' ',text)
    return text_2
    

# spaCy summariser
def summariser_spacy(raw_doc):
    raw_text = raw_doc
    doc = nlp(source_text)
    stopwords = list(STOP_WORDS)
    word_frequencies = {}  
    for word in doc:  
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    sentence_list = [ sentence for sentence in doc.sents ]

    sentence_scores = {}  
    for sent in sentence_list:  
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 100:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    summary_sentences = nlargest(10, sentence_scores, key=sentence_scores.get)
    final_sentences = [ w.text for w in summary_sentences ]
    summary = ' '.join(final_sentences)
    return(summary)
    
