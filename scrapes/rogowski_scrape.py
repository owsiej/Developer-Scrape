from bs4 import BeautifulSoup
import requests
from standardize_flat_info import standardize_status, summarize

baseUrl='https://www.rogowskidevelopment.pl/'


response=requests.get(f'{baseUrl}')
startSoup=BeautifulSoup(response.text, "html.parser")


def get_all_developer_invests(scrape: BeautifulSoup):
    """# get names of all investments and links to them from front page
    Args:
        scrape (BeautifulSoup): object ready to scrape

    Returns:
        all investments of developer in list
    """
    result=[]

    investments=scrape.find(class_='home-boxes no-gutter row').find_all('a')

    for investment in investments:
        if investment.find(class_='box-city'):
            if investment.find(class_='box-city').get_text()=='Białystok':
                result.append({
                    'name':investment['title'],
                    'link':investment['href']
                })

    return result



def get_invests_ids():
    """get ids of all investments

    Args:
        investments (list): investments to which we need to get ids
    Returns:
        lists of all buildings in all investments with ids
    """
    investments=get_all_developer_invests(startSoup)
    listOfIds=[]

    for invest in investments:
        investResponse=requests.get(f"{invest['link']}")
        investSoup=BeautifulSoup(investResponse.text, "html.parser")

        ids=investSoup.select('[data-id]')
        for id_ in ids:
            listOfIds.append({'name':id_.get_text().strip(),
                                        'id':id_['data-id'],
                                        'type': 'flat'
                                        })
       
#Horodniany to jedyne domy i żeby api zadziałało trzeba zmienić type na house
    listOfIds[4]['type']='house'
    
    return listOfIds


def get_flats_info():

    buildings=get_invests_ids()
    flatsList=[]
    sumUp=[]
    for building in buildings:

        
        baseApi="https://www.rogowskidevelopment.pl/wp-json/wp/v2/flat?filter[meta_key_value_compare]" \
                f"[stage][{building['id']}]==&filter[meta_key_value_compare][object_type]" \
                f"[{building['type']}]==&filter[meta_key_value_compare][state][inactive]=!=&filter[posts_per_page]=-1"

        response=requests.get(f'{baseApi}')
        flats=response.json()
        
        temporaryList=[]
            
        for flat in flats:
            temporaryList.append({
                    'flat_name':building['name'],
                    'floor_number':flat['floor_number'][0]['floor_number'],
                    'rooms_number':flat['rooms'],
                    'area':float(flat['sqm']),
                    'price':float(flat['price']),
                    'status':standardize_status(flat['state'][0])
                })
        flatsList.append(temporaryList)
        sumUp.append(summarize(temporaryList))
    return flatsList, sumUp


