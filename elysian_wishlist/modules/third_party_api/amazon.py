from bs4 import BeautifulSoup
import requests
import json

def amazon_search_catalog(query, page):
    """Get a list of items from amazon's catalogue based on the query and page parameter.
    
    Parameters:
    -----------
    query: str
        The search text amazon's catalogue.
    page: int
        The page number of the catalogue you want to see.
        
    Returns:
    --------
    A json object.
    """

    #getting the webpage
    url='https://www.amazon.com/s?k='+query.replace(' ', '+')+'&page='+str(page)
    headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0", "Accept-Encoding":"gzip, deflate, br", "Accept":"text/html, */*; q=0.01", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    data=requests.get(url, headers=headers).text
    soup=BeautifulSoup(data, 'html.parser')
    
    #initializing a list to store all dicts
    list=[]
    
    #looping through the webpage to get the relevant info
    for i in soup.find_all('span', class_='celwidget slot=MAIN template=SEARCH_RESULTS widgetId=search-results'):
        try:
            title=i.find('span', class_='a-size-base-plus a-color-base a-text-normal').get_text()
            price=i.find('span', class_='a-offscreen').get_text()
            image=(i.img['srcset'].split(',')[-1])[1:-2]
            item_id=(i.find('div', class_='a-row a-size-small').find('span', class_='a-declarative'))['data-a-popover'].split(',')[-1].split('&')[1].replace('asin=', '')
            link='https://www.amazon.com/dp/'+item_id
            
            #make sure price has $ in it
            for i in price:
                if i == '$':
                    break
            else:
                continue
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
    
def amazon_search_item(item_id):
    """Get information about an item based on id.
    
    Parameters:
    -----------
    item_id: str
        The id for an item on amazon.
        
    Returns:
    --------
    A json object.
    """
    
    #getting the webpage
    url='https://www.amazon.com/dp/'+str(item_id)
    headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0", "Accept-Encoding":"gzip, deflate, br", "Accept":"text/html, */*; q=0.01", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    
    data=requests.get(url, headers=headers).text
    soup=BeautifulSoup(data, 'html.parser')
    
    #extract variables from the webpage
    title=soup.find('span', id='productTitle').get_text().replace('\n', '')
    image=soup.find('img', id='landingImage')['data-old-hires']
    price=soup.find('span', id='priceblock_ourprice').get_text()

    
    return json.dumps({
        'item_id': item_id,
        'title': title,
        'price': price,
        'link': url,
        'image': image,
    })
    
