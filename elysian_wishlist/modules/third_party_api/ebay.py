from bs4 import BeautifulSoup
import requests
import json

def ebay_search_catalog(query, page):
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
    data=requests.get(url).text
    soup=BeautifulSoup(data, 'html.parser')

    #initializing a list to store all dicts
    list=[]

    #looping through the webpage to get the relevant info
    for i in soup.find_all('li', class_='s-item s-item--watch-at-corner'):
        try:
            title=i.h3.get_text()
            price=i.find('span', class_='s-item__price').get_text()
            link=i.a['href']
            item_id=link.split('/')[-1].split('?')[0]
            link='https://www.ebay.com/itm/'+item_id
            image=i.find('img', class_='s-item__image-img')['src']
        except:
            continue
        list.append({
            'item_id': item_id,
            'title': title,
            'price': price,
            'link': link,
            'image': image,
        })

    return json.dumps(list)

def ebay_search_item(item_id):
    """Get information about an item based on id.

    Parameters:
    -----------
    item_id: int
        The id number for an item on ebay.

    Returns:
    --------
    A dictionary contains relevant information for the item.
    """

    #getting the webpage
    url='https://www.ebay.com/itm/'+str(item_id)
    data=requests.get(url).text
    soup=BeautifulSoup(data, 'html.parser')

    #extract variables from the webpage
    title=soup.find('h1', id='itemTitle').get_text().replace('Details about   ', '')
    image=soup.find('img', id='icImg')['src']
    price=soup.find('span', id='prcIsum').get_text()

    return json.dumps({
        'item_id': item_id,
        'title': title,
        'price': price,
        'link': url,
        'image': image,
    })
