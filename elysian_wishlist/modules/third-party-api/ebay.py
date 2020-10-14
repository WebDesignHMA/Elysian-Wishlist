from bs4 import BeautifulSoup
import asyncio
import aiohttp


async def get_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text() 

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
    data=await get_data(url)
    soup=BeautifulSoup(data, 'html.parser')
    
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
        item_id=link.split('/')[-1].split('?')[0]
        link='https://www.ebay.com/itm/'+item_id
        image=i.find('img', class_='s-item__image-img')['src']
        
        list.append({
            'item_id': item_id,
            'title': title,
            'condition': condition,
            'price': price,
            'shipping': shipping,
            'link': link,
            'image': image,
        })   
      
    return list
    
async def search_item(item_id):
    #getting the webpage
    url='https://www.ebay.com/itm/'+str(item_id)
    data=await get_data(url)
    soup=BeautifulSoup(data, 'html.parser')
    
    #extract variables from the webpage
    title=soup.find('h1', id='itemTitle').get_text().replace('Details about   ', '')
    image=soup.find('img', id='icImg')['src']
    price=soup.find('span', id='priceIsum').get_text()
    shipping=
    condition
    description
    rating
    
    return 
    
print(asyncio.run(search_item(item_id=184453248228)))
