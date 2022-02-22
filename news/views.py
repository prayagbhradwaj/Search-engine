from django.shortcuts import render,redirect
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
# Create your views here.

class search_bar(forms.Form):
    query = forms.CharField(label="")

tasks = []


session = requests.Session()
session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
url = "https://www.hindustantimes.com/"
content = session.get(url, verify=False).content
soup = BSoup(content, "html.parser")




def real_query(var):
     docs = doc
     vectorizer = TfidfVectorizer()
     X = vectorizer.fit_transform(docs)
     df = pd.DataFrame(X.T.toarray(), index=vectorizer.get_feature_names())
     print(df.head())
     print(df.shape)
     q1 = var
     get_similar_articles(q1, df,docs,vectorizer)
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
     it = 0
     for urls in list_of_links:
          content_ = session.get(urls, verify=False).content
          soup_ = BSoup(content_, "html.parser")
          if it == 2:
              break
          try:
              heading = soup_.find('h1',class_='hdg1').text
              description = soup_.find('div',class_='detail')  
              it = it + 1        
          except AttributeError as error:
              print("we won")          
          else:
              doc_ = ""
              try:
                  for t in description.find_all('p'):
                      doc_ = doc_ + t.text
              except AttributeError as error:
                  print("we 22")
              else:
                  doc.append(doc_)                          
               
          #temp_list = []


def clean_the_code(tdoc):
     documents_clean = []
     for d in tdoc:
         document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)
         document_test = re.sub(r'@\w+', '', document_test)
         document_test = document_test.lower()
         document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
         document_test = re.sub(r'[0-9]', '', document_test)
         document_test = re.sub(r'\s{2,}', ' ', document_test)
         documents_clean.append(document_test)
     return documents_clean

def here_we_go(variable):
    it = 0
    
    doc = []
    try:
        heading = soup.find('h1',class_='hdg1').text
        description = soup.find('div',class_='detail')
    except AttributeError as error:
        print("sdf")          
    else:
        for t in description.find_all('p'):
            doc.append(t.text)
    list_of_links = crawl_retun_list()
    doc_list = []
    it = 0
    for urls in list_of_links:
        content_ = session.get(urls, verify=False).content
        soup_ = BSoup(content_, "html.parser")
        if it == 10:
            break
        try:
            heading = soup_.find('h1',class_='hdg1').text
            description = soup_.find('div',class_='detail')  
            it = it + 1        
        except AttributeError as error:
            print("we won")          
        else:
            doc_ = ""
            try:
                for t in description.find_all('p'):
                    doc_ = doc_ + t.text
            except AttributeError as error:
                print("we 22")
            else:
                doc.append(doc_)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(doc)

    df = pd.DataFrame(X.T.toarray(), index=vectorizer.get_feature_names())
    print(df.head())
    print(df.shape)

    def similar_articles(q, df):
        print("query:", q)
        print("Performing checks : ")
        q = [q]
        q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
        sim = {}
        for i in range(10):
            sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
        
        sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
        
        for k, v in sim_sorted:
            if v != 0.0:
                print("Similarties are:", v)
                print(doc[k])
                tasks.append(doc[k])
                print()

    similar_articles(variable, df)

print("\n")
print("starts\n")
'''for i in doc:
    print(i,end="\n")'''
def index(request):
    return render(request, "news/results.html", {
        "tasks": tasks
    })
def home(request):
    if request.method == "POST":
        form = search_bar(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            
            """dfs_traverse()
            clean_the_code()
            real_query(query)
            tasks.append(query)"""
            here_we_go(query)

            return HttpResponseRedirect(reverse("news:index"))
        else:
            return render(request, "news/index.html", {
                "form": form
            })
    return render(request, "news/index.html", {
        "form": search_bar()
    })


    
"""def crawl_retun_list():
     link = []
     for i in soup.find_all('a',href=True):
          temp = i['href']
          if temp[0] == '/':
               var = 'https://www.hindustantimes.com' + temp
               link.append(var)
     return link"""
'''def news_list(request):
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
'''