from bs4 import BeautifulSoup
import requests
import re
from standardize_flat_info import summarize

def get_flats_info():
    
    baseUrl='https://www.butikowa-kamienica.pl/apartamenty.html'
    response=requests.get(baseUrl)
    soup=BeautifulSoup(response.text, "html.parser")

    pattern=re.compile(r'popup\d+')
    match=pattern.search('popup12312')


    floors=soup.find(class_='ps614 v37 s540').find_all('div')
    matches=pattern.findall(str(floors))


    flatsList=[]
    flatNames=[]
    
    for match in set(matches):
        for floor in floors:
            flat=floor.find(id=match)
            if flat is not None:
                name=flat.p.get_text()
                if name and name not in flatNames:
                    
                    flatsList.append({
                    'flat_name':name,
                    'floor_number':'',
                    'rooms_number':flat.p.find_next_sibling().get_text().split()[2],
                    'area':float(flat.p.find_next_sibling().find_next_sibling().get_text().split()[1].replace('m2', '').replace(',', '.').strip()),
                    'price':'no-info',
                    'status':flat.p.find_next_sibling().find_next_sibling().find_next_sibling().get_text().split()[1],
                })
                    flatNames.append(name)
                    
    flatsList=sorted(flatsList, key= lambda item: int(item['flat_name'].split()[1][1:]))
    for flat in flatsList:
        flat['flat_name']='Butikowa Kamienica'

    sumUp=[summarize(flatsList)]

    return [flatsList], sumUp
