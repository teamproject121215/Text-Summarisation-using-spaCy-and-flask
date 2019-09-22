from __future__ import unicode_literals
from flask import Flask,render_template,url_for,request
from heapq import nlargest
import re
import os
from werkzeug.utils import secure_filename

import spacy
nlp = spacy.load('en_core_web_lg')
from spacy.lang.en.stop_words import STOP_WORDS
stopwords = list(STOP_WORDS)
from string import punctuation
app = Flask(__name__)


# Web Scraping Pkg
from bs4 import BeautifulSoup
# from urllib.request import urlopen
import urllib.request

#summarizer
def summariser_spacy(raw_docx):
    raw_text = raw_docx
    docx = nlp(raw_text)
    stopwords = list(STOP_WORDS)
    word_frequencies = {}  
    for word in docx:  
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    sentence_list = [ sentence for sentence in docx.sents ]

    sentence_scores = {}  
    for sent in sentence_list:  
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 100:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    summary_sentences = nlargest(15, sentence_scores, key=sentence_scores.get)
    final_sentences = [ w.text for w in summary_sentences ]
    summary = ' '.join(final_sentences)
    return(summary)

#cleaning function
def clean_text(t1):
    t1=re.sub(r'\[[0-9]*\]',' ',t1)               ####removing brackets and extra spaces
    t1=re.sub(r'\s+',' ',t1)
    t2=t1
    t2=re.sub('[^a-zA-Z]',' ',t1)        ####removing special characters and digits
    t2=re.sub(r'\s+',' ',t1)
    return t2

# Fetch Text From Url
def text_from_url(URL):
    article=urllib.request.urlopen(URL)
    parsed_article=BeautifulSoup(article,'html')
    paragraphs=parsed_article.find_all('p')
    article_text=" "
    for p in paragraphs:
        article_text += p.text
    return(str(article_text))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploads',methods=['GET','POST'])
def uploads():
    if request.method == 'POST' and 'txt_data' in request.files:
        file = request.files['txt_data']
        choice = request.form['saveoption']
        filename = summariser_spacy(choice)
        file.save(os.path.join('C:/',filename))
        return render_template('index.html',filename=filename)


@app.route('/url_text',methods=['GET','POST'])
def url_text():
    if request.method == 'POST':
        raw_url = request.form['raw_url']
        raw_text = text_from_url(raw_url)
        cleaned_text = clean_text(raw_text)
        summary_scraped = summariser_spacy(cleaned_text)
        return render_template('index.html',summary_scraped=summary_scraped)


@app.route('/about')
def about():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)