from flask import Flask, render_template
import html5lib
import requests
from bs4 import BeautifulSoup


#ESPN Requests
r1 = requests.get('https://www.espn.com/nba/')
coverpage = r1.content
soup1 = BeautifulSoup(coverpage, 'html5lib')
#news_cards_espn = soup1.findAll('ul', class_='headlineStack__list')
news_cards_espn = soup1.find_all('section', class_='headlineStack__listContainer')
headlines_found = False
index = 0
while(not headlines_found):
    temp_headlines = news_cards_espn[index].find_all('li')
    if (len(temp_headlines) > 5):
        news_cards_espn = temp_headlines
        headlines_found = True
    else:
        index += 1
article_titles_espn = []
article_links_espn = []
for i in range(0, len(news_cards_espn) - 1):
    article = news_cards_espn[i]
    article_titles_espn.append(article.a.text)
    if (i != 1): 
        article_links_espn.append('https://www.espn.com' + (article.a.get('href')))
    else: 
        article_links_espn.append(article.a.get('href')) 


#Bleacher Report Requests
r2 = requests.get('https://bleacherreport.com/nba')
coverpage_br = r2.content
soup2=BeautifulSoup(coverpage_br, 'html5lib')
news_cards_br = soup2.find_all('a', class_='atom articleTitle')
article_titles_br = []
article_links_br = []
for i in range (len (news_cards_br)):
    article = news_cards_br[i]
    article_titles_br.append(article.h3.text)
    article_links_br.append(article.get('href'))
    

#The Athletic Requests
r3 = requests.get('https://theathletic.com/nba/')
coverpage_athletic = r3.content
soup3 = BeautifulSoup(coverpage_athletic, 'html5lib')
news_cards_ath = soup3.find_all('div', class_='MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 MuiGrid-wrap-xs-nowrap')
article_links_ath = []
article_titles_ath = []
for i in range (len(news_cards_ath)):
    article = news_cards_ath[i]
    article_titles_ath.append(article.span.text)
    article_links_ath.append(article.a.get('href'))


#NBA.com Requests
r4 = requests.get('https://www.nba.com/')
coverpage_nba = r4.content
soup4 = BeautifulSoup(coverpage_nba, 'html5lib')
news_cards_nba = soup4.find('div', class_='Block_blockContainer__2tJ58')
news_cards_nba = news_cards_nba.find_all('li')
article_links_nba = []
article_titles_nba = []
for i in range (1, len(news_cards_nba)):
    article = news_cards_nba[i]
    article_titles_nba.append(article.a.text)
    article_links_nba.append('https://www.nba.com/' + (article.a.get('href')))


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', len_espn = len(article_titles_espn), article_titles_espn = article_titles_espn, article_links_espn = article_links_espn, 
        len_br = len(article_titles_br), article_titles_br = article_titles_br, article_links_br = article_links_br,
        len_ath = (len(article_links_ath )), article_links_ath  = article_links_ath, article_titles_ath = article_titles_ath,
        len_nba = len(article_titles_nba), article_titles_nba = article_titles_nba, article_links_nba = article_links_nba)

if __name__ == "__main__":
    app.run(debug=True)

