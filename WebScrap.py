import urllib.request
from bs4 import BeautifulSoup
from newspaper import Article
import csv
import nltk
import time
import pandas as pd
import re

words = ["surge", "acquisitions", "IPO", "initial public offering", "surge.", "acquisitions.", "IPO.",
         "initial public offering."]

def find_keyword(text):
    text=text.replace("\n\n"," ")
    text=text.replace("\n"," ")
    check=text.split(" ")
    pos1 = 0
    pos2 = 0
    for i in check:
        if i in words:
            for j in range(check.index(i) - 1, -1, -1):
                if "." in check[j][-1]:
                    pos1 = j + 1
                    break
            for j in range(check.index(i), len(check)):
                if "." in check[j][-1]:
                    pos2 = j + 1
                    break
            s=" ".join(check[pos1:pos2])
            if "\n" in s:
                print(s[s.index("\n"):])
            else:
                print(s)

nltk.download('punkt')
url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN%3Aen"

page = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
infile = urllib.request.urlopen(page).read()
soup = BeautifulSoup(infile, 'lxml')
section = soup.find("div", {"class":"tsldL Oc0wGc"}) #tsldL Oc0wGc, xrnccd F6Welf R7GTQ keNKEd j7vNaf

k=0
main_news_title=[]
main_news_summary=[]
main_news_datetime=[]
main_news_url=[]

sub_news_title=[]
sub_news_summary=[]
sub_news_datetime=[]
sub_news_url=[]

x = section.find_all("div",attrs={"class":"xrnccd F6Welf R7GTQ keNKEd j7vNaf"})

for i in x:
    k+=1
    #main news

    a=i.find("a",attrs={"class":"VDXfz", "jsname": "hXwDdf"})

    article1 = Article("https://news.google.com"+a['href'][1:], language="en")
    try:
        article1.download()
    except:
        continue
    article1.parse()
    article1.nlp()

    main_news_title.append(article1.title)
    main_news_summary.append(article1.summary)
    main_news_datetime.append(article1.publish_date)
    main_news_url.append("https://news.google.com"+a['href'][1:])


    #sub news

    m=i.find("div",attrs={"class":"SbNwzf","jsname":"GNGJO"})
    b=m.find("a",attrs={"class":"VDXfz", "jsname": "hXwDdf"})

    article2 = Article("https://news.google.com" + b['href'][1:], language="en")
    try:
        article2.download()
    except:
        continue
    article2.parse()
    article2.nlp()
    sub_news_title.append(article2.title)
    sub_news_summary.append(article2.summary)
    sub_news_datetime.append(article2.publish_date)
    sub_news_url.append("https://news.google.com" + b['href'][1:])

    #print sentences that have keywords in it
    find_keyword(article1.text)
"""
    if k>10:
        print("10 articles done.")
        break
"""

main_news = pd.DataFrame({'News Title':main_news_title,'Summarized News Text':main_news_summary,'Datetime':main_news_datetime,'URL':main_news_url})
main_news.to_csv('Main News.csv', index=False, encoding='utf-8')

sub_news = pd.DataFrame({'News Title':sub_news_title,'Summarized News Text':sub_news_summary,'Datetime':sub_news_datetime,'URL':sub_news_url})
sub_news.to_csv('Sub News.csv', index=False, encoding='utf-8')


