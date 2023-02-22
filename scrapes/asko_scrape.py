from bs4 import BeautifulSoup
import requests
from standardize_flat_info import standardize_status, str_to_float, summarize



def get_all_developer_invests(url):
    """# get names of all investments and links to them from front page
    Args:
        scrape (BeautifulSoup): object ready to scrape

    Returns:
        all investments of developer in list
    """
    result=[]
    response=requests.get(f'{url}')

    soup=BeautifulSoup(response.text, "html.parser")
    data=soup.find_all(class_='properties__info')
    
    for item in data:
        result.append({'name':item.find(class_='properties__address-street').get_text(),
                      'link': item.a['href']})
    
    return result


def get_flats_info():
    """get infos of all flats

    Args:
        all_buildings (list): list of all buildings with ids used in api

    Returns:
        list with infos of all flats developer has got
    """

    buildings=get_all_developer_invests(baseUrl)
    
    flatsList=[]
    sumUp=[]

    for building in buildings:

        
        response=requests.get(f"{building['link']}")
        soup=BeautifulSoup(response.text, "html.parser")
        flats=soup.tbody.find_all('tr')
        
        temporaryList=[]
        for flat in flats:
            temporaryList.append({
                'flat_name':building['name'],
                'floor_number':flat.td.find_next_sibling().find_next_sibling().find_next_sibling().get_text(),
                'rooms_number':flat.td.find_next_sibling().find_next_sibling().get_text(),
                'area':str_to_float(flat.td.find_next_sibling().get_text().replace('m2', '').strip()),
                'price':str_to_float(flat.td.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text().replace('zł', '').replace(' ', '').strip()),
                'status':standardize_status(flat.td.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()),
            })
        flatsList.append(temporaryList)
        sumUp.append(summarize(temporaryList))
    return flatsList, sumUp
    



baseUrl='https://askosa.pl/inwestycja'

# aLLBuildings=get_all_developer_invests(baseUrl)
# allFlatsInBuildings,summarizedFlatsInfos=get_flats_info(aLLBuildings)

# get_csv(allFlatsInBuildings, 'asko_flats.csv')


