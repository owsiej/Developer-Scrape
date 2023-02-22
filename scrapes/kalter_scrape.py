from bs4 import BeautifulSoup
import requests
from standardize_flat_info import standardize_status, summarize

def get_all_developer_invests(url):

    response=requests.get(url)
    soup=BeautifulSoup(response.text , "html.parser")

    result=[]

    flats=soup.find_all('div', class_='col-12 col-md-6')
    for flat in flats:
        city=flat.find('span', class_='d-flex align-items-center justify-content-center').get_text()
        if city=='Białystok':
            result.append({'name':flat.a.h2.get_text(),
            'link':flat.a['href']})
    
    return result

def get_flats_info():
    
    buildings=get_all_developer_invests(baseUrl)
    flatsList=[]
    sumUp=[]

    for building in buildings:
        
        params={'s_pietro':'',
                's_pokoje':'',
                's_typ':1,
                's_status':'',
                's_metry':'',
                's_aneks':'',
                's_garden':'',
                's_deck':'',
                'a':'szukaj'}

        response=requests.get(building['link'], params)
        soup=BeautifulSoup(response.text, "html.parser")
        first_flat=soup.find('div', id='offerList').find('div', class_='row').find_next()
        flats=first_flat.find_next_siblings()
        flats.insert(0,first_flat)
        temporaryList=[]
        for flat in flats:
            if flat.span.get_text()=='Mieszkanie':
                temporaryList.append({
                'flat_name':building['name'],
                'floor_number':int(flat.find('li', class_='li-inwest-rwd').span.get_text()),
                'rooms_number':int(flat.li.span.get_text()),
                'area':float(flat.li.span.find_next('span').get_text().replace('m2', '').strip().replace(',', '.')),
                'price':'no-info',
                'status':standardize_status(flat.find('div', class_='col text-center').get_text().strip())})
        flatsList.append(temporaryList)
        sumUp.append(summarize(temporaryList))
        
    return flatsList,sumUp
    
baseUrl='https://www.kalternieruchomosci.pl/pl/oferta-mieszkan'







