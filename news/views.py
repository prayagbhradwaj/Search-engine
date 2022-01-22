import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
# Create your views here.
session = requests.Session()
session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
url = "https://www.hindustantimes.com/cricket/is-the-glass-half-full-or-half-empty-vvs-laxman-and-aakash-chopra-have-their-say-on-virat-kohli-and-cheteshwar-pujara-s-century-droughts-101638761380709.html"
content = session.get(url, verify=False).content
soup = BeautifulSoup(content, "html.parser")
heading = soup.find('h1',class_='hdg1').text
description = soup.find('div',class_='detail')
doc = []
for t in description.find_all('p'):
     doc.append(t.text)
def scrape(request):  
    return redirect("../")
def clean_the_code():
     documents_clean = []
     for d in doc:
         document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)
         document_test = re.sub(r'@\w+', '', document_test)
         document_test = document_test.lower()
         document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
         document_test = re.sub(r'[0-9]', '', document_test)
         document_test = re.sub(r'\s{2,}', ' ', document_test)
         documents_clean.append(document_test)
     return documents_clean
def get_similar_articles(q, df,docs):
  print("query:", q)
  print("What im doin in life: ")
  q = [q]
  q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
  sim = {}
  for i in range(10):
    sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
  
  sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
  
  for k, v in sim_sorted:
    if v != 0.0:
      print("Similarties are :", v)
      print(docs[k])
      print()


docs = clean_the_code()
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(docs)
df = pd.DataFrame(X.T.toarray(), index=vectorizer.get_feature_names())
print(df.head())
print(df.shape)
q1 = 'about'
get_similar_articles(q1, df,docs)
print('-'*100)


def crawl_retun_list():
     link = []
     for i in soup.find_all('a',href=True):
          temp = i['href']
          if temp[0] == '/':
               var = 'https://www.hindustantimes.com' + temp
               link.append(var)
     return link

def get_similar_articles(q, df,docs):
  print("query:", q)
  print("What im doin in life: ")
  q = [q]
  q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
  sim = {}
  for i in range(10):
    sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
  
  sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
  
  for k, v in sim_sorted:
    if v != 0.0:
      print("Similarties are :", v)
      print(docs[k])
      print()

def real_query():
     docs = clean_the_code()
     vectorizer = TfidfVectorizer()
     X = vectorizer.fit_transform(docs)
     df = pd.DataFrame(X.T.toarray(), index=vectorizer.get_feature_names())
     print(df.head())
     print(df.shape)
     q1 = 'about'
     get_similar_articles(q1, df,docs)
     print('-'*100)

def crawl_retun_list():
     link = []
     for i in soup.find_all('a',href=True):
          temp = i['href']
          if temp[0] == '/':
               var = 'https://www.hindustantimes.com' + temp
               link.append(var)
          elif temp[0] == 'h' and temp[1] == 't' and temp[2] == 't' and temp[3] == 'p' and temp[4] == 's' and temp[5] == ':' and temp[6] == '/' and temp[7] == '/' and temp[8] == 'w' and temp[9] == 'w' and temp[10] == 'w' and temp[11] == '.' and temp[12] == 'h' and temp[13] == 'i' and temp[14] == 'n' and temp[15] == 'd' and temp[16] == 'u':
              link.append(temp)
     return link
def dfs_traverse():
     list_of_links = crawl_retun_list()
     doc_list = []
     for urls in list_of_links:
          content_ = session.get(urls, verify=False).content
          soup_ = BeautifulSoup(content_, "html.parser")
          heading = soup_.find('h1',class_='hdg1').text
          description = soup_.find('div',class_='detail')
          doc = ""
          for t in description.find_all('p'):
               doc = doc + t.text
          temp_list = []
          temp_list.append(doc)

def news_list(request):
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = "https://www.hindustantimes.com/"
    content = session.get(url, verify=False).content
    soup = BSoup(content, "html.parser")
    results = soup.find_all('div',class_='dateTime')
    for i in results:
        title = i.text
        date = i.text
        new_headline = Headline()
        new_headline.title = title
        new_headline.date = title
        new_headline.save()
        headlines = Headline.objects.all()
    context = {
        'object_list': headlines,
    }
    return render(request, "news/index.html", context)
