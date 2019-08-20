#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 18:00:07 2019

@author: smkj33
"""



"""
Previous Version: 
    bkp_model_20_Aug.py

-- Removing html filter using HTML.parser 
-- Removing related import statement
-- Beautiful soup will be used in it's place'

"""


import pandas as pd

# TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer


# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel


from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer


# Requried for connection to MySQL db
import pymysql
from db_config import *


# DB Queries generated in here
from queries import *

from bs4 import BeautifulSoup


import re



def import_content ():

    try:
        conn = pymysql.connect(**connection_properties)
        sql = importContentQuery()
        df = pd.read_sql(sql, conn)

        #closing database connection.
        if(conn.open):
            conn.close()
            print("MySQL connection is closed")

        return df

    except Exception as e :
        print ("Error while connecting to MySQL", e)










def text_filter_html(article_master):
    article_master['reduced_content'] = article_master.apply(
            lambda row: strip_tags(row.bodytext).lower(), axis = 1)
    return article_master

    # pd.set_option('max_colwidth', 100)
    # print(article_master['reduced_content'])


# def text_soup_filter(text):
def text_soup_filter(text):
    soup = BeautifulSoup(text, features="html5lib")
    text = re.sub('[^a-z\s]', '',soup.get_text(separator=' ').lower())
    return text





def text_stemmer(article_master, porter):
    # The following line produces the stem of every word and then removes all non alphabet characters
    article_master['stemmed_content'] = article_master.apply(lambda row: porter_stemmer(re.sub('[^a-z\s]', '', row.reduced_content), porter), axis = 1)
    article_master['stemmed_content'] = article_master['stemmed_content'].fillna('')
    return article_master


def porter_stemmer (txt, porter):
    token_words=word_tokenize(txt)
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)


# def calculate_frequency (article_master):
#     #Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
#     tfidf = TfidfVectorizer(stop_words='english')




article_master = import_content()
# print(article_master)
article_master = text_filter_html(article_master)
print(article_master)



# article_master['reduced_content'] = article_master.apply(
#             lambda row: text_soup_filter(row.bodytext), axis = 1)

article_master['reduced_content'] = article_master.apply(
        lambda row: BeautifulSoup(row.bodytext).get_text().lower(), axis = 1)
print(article_master)

# porter = PorterStemmer()
# article_master = text_stemmer(article_master, porter)
# print(article_master)