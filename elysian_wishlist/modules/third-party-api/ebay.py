#Ebay URL generator
#https://www.ebay.com/sch/i.html?
#& between each parameter
#_nkw=KEYWORDS+FOR+SEARCH
#_pgn=1
from bs4 import BeautifulSoup
import requests

url='https://www.ebay.com/sch/i.html?'
search=input("Search:")
print(search)
pgn=1
output=url+'_nkw='+search.replace(' ', '+')+'&_pgn='+str(pgn)

soup=BeautifulSoup(requests.get(output).text, 'html.parser')
for i in soup.find_all("li", class_="s-item s-item--watch-at-corner"):
    print("Link to item:")
    print(i.a["href"])
    print("Link to image:")
    print(i.find("img", "s-item__image-img")["src"])
    print("************************************************************************")




