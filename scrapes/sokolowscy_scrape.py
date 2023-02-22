from bs4 import BeautifulSoup
import requests
from standardize_flat_info import standardize_status, str_to_float, summarize

baseUrl='https://sokolowscynieruchomosci.pl/w-sprzedazy'


def get_all_developer_invests(url=baseUrl):

    response=requests.get(url)
    soup=BeautifulSoup(response.text, "html.parser")

    investments=soup.find_all('div', class_='col-12 col-md-6 col-lg-4 mt-3')

    result=[]

    for investment in investments:    
        if investment.find('h5', class_="color-dark-silver").get_text()!='Brak dostępnych':
            result.append({'name':investment.find('h5').get_text(),
                        'link': investment.a['href']})

    return result

def get_flats_info():
    
    buildings=get_all_developer_invests()
    sumUp=[]
    flatsList=[]
    for building in buildings:
        url=building['link']
        response=requests.get(url)
        soup=BeautifulSoup(response.text, "html.parser")

        flats=soup.tbody.find_all('tr')

        temporaryList=[]
        for flat in flats:
            infos=flat.find_all('a')
            temporaryList.append({
                'flat_name':building['name'],
                'floor_number':'-',
                'rooms_number':infos[2].get_text(),
                'area':float(infos[1].get_text().replace('m2', '').strip()),
                'price':str_to_float(infos[4].get_text().replace('zł', '').strip().replace(' ', '')),
                'status':standardize_status(flat.find_all('td')[-1].get_text())
            })
        flatsList.append(temporaryList)
        sumUp.append(summarize(temporaryList))
        
    return flatsList, sumUp
