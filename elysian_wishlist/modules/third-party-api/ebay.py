from bs4 import BeautifulSoup
import requests
import asyncio

async def search_catalog(query, page):
    """Get a list of items from ebay's catalogue based on the query and page parameter.
    
    Parameters:
    -----------
    query: str
        The search text ebay's catalogue.
    page: int
        The page number of the catalogue you want to see.
        
    Returns:
    --------
    A list of dictionaries where each dictionary contains relevant information for each item.
    """

    #getting the webpage
    url='https://www.ebay.com/sch/i.html?_nkw='+query.replace(' ', '+')+'&_pgn='+str(page)
    soup=BeautifulSoup(requests.get(url).text, 'html.parser')
    
    #initializing a list to store all dicts
    list=[]
    
    #looping through the webpage to get the relevant info
    for i in soup.find_all('li', class_='s-item s-item--watch-at-corner'):
        title=i.h3.get_text()
        condition=None #condition isn't always displayed.
        try:
            conidtion=i.find('span', class_='SECONDARY_INFO').get_text()
        except:
            pass
        price=i.find('span', class_='s-item__price').get_text()
        shipping=i.find('span', class_='s-item__shipping s-item__logisticsCost').get_text()
        link=i.a['href']
        image=i.find('img', class_='s-item__image-img')['src']
        
        list.append({
            'title': title,
            'condition': condition,
            'price': price,
            'shipping': shipping,
            'link': link,
            'image': image,
        })   
      
    return list
