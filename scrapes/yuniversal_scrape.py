from bs4 import BeautifulSoup
import requests
from standardize_flat_info import standardize_status, standardize_floor_number, str_to_float, summarize

baseUrl='https://www.yuniversalpodlaski.pl/'
cityTag='#Bialystok'

def get_all_developer_invests(url=baseUrl, tag=cityTag):
    """# get names of all investments and links to them from front page
    Args:
        scrape (BeautifulSoup): object ready to scrape

    Returns:
        all investments of developer in list
    """
    result=[]

    
    response=requests.get(f'{url}{tag}')
    soup=BeautifulSoup(response.text, "html.parser")
        
    investments=soup.find_all(attrs={'data-city':'Bialystok'})
 
    for investment in investments:
        try:
            result.append({'name':investment.find(class_='nazwa').get_text().encode('iso-8859-1').decode('utf-8'),
                           'link':investment['href']})
        except AttributeError:
            pass
    return result


def get_flats_info(url=baseUrl):
    """get infos of all flats

    Args:
        all_buildings (list): list of all buildings with ids used in api

    Returns:
        list with infos of all flats developer has got
    """
    buildings=get_all_developer_invests()
    flatsList=[]
    sumUp=[]

    
    for building in buildings:
        response=requests.get(f"{url}{building['link']}")
        soup=BeautifulSoup(response.text, "html.parser")
        temporaryList=[]                   
        try:
            flats=soup.tbody.tr.find_next_siblings()
            flats.append(soup.tbody.tr)
            flats.sort(key= lambda item: (len(item.find(class_='t_numer').get_text()),item.find(class_='t_numer').get_text()))
        except AttributeError:
            pass
        else:
            for flat in flats:

                temporaryList.append({
                    'flat_name':building['name'],
                    'floor_number':standardize_floor_number(flat.find(class_='t_pietro').get_text()),
                    'rooms_number':flat.find(class_='t_pokoje').get_text(),
                    'area':float(flat.find(class_='t_metraz').get_text().replace('m²', '').strip()),
                    'price':str_to_float(flat.find(class_='t_cena').get_text().split('PLN')[0].strip().replace(',','.').replace(' ', '')),
                    'status':standardize_status(flat.find(class_='t_metraz').find_next_sibling().get_text().encode('iso-8859-1').decode('utf-8'))
                })
            flatsList.append(temporaryList)
            sumUp.append(summarize(temporaryList))
    return flatsList, sumUp
