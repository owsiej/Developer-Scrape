from bs4 import BeautifulSoup
import requests
from standardize_flat_info import str_to_float,summarize

baseUrl='https://www.jaz-bud.pl'

cityTag='/bialystok'



def get_all_developer_invests(url):

    response=requests.get(url)
    soup=BeautifulSoup(response.text, "html.parser")

    investments=soup.body.section.find_all('a')
    result=[]
    for investment in investments:     
        result.append({'name':"".join(investment.get_text().split(',')[1:]).strip(),
                      'link':investment['href']})

    return result

def get_flats_info(url=baseUrl):

    buildings=get_all_developer_invests(baseUrl+cityTag)
    sumUp=[]
    flatsList=[]

    for building in buildings:
        urlTag=building['link']
        response=requests.get(url+urlTag)
        soup=BeautifulSoup(response.text, "html.parser")
        flats=soup.tbody.find_all('tr')

        temporaryList=[]
        while True:
            for flat in flats:
                cursor=flat.find(class_='fa fa-search').find_parent().find_parent()
                temporaryList.append({
                        'flat_name':building['name'],
                        'floor_number':cursor.find_previous_sibling().find_previous_sibling().find_previous_sibling().get_text(),
                        'rooms_number':cursor.find_previous_sibling().find_previous_sibling().get_text(),
                        'area':float(cursor.find_previous_sibling().find_previous_sibling().find_previous_sibling().find_previous_sibling().get_text().replace('m2', '').replace(",", '.').strip()),
                        'price':str_to_float(cursor.find_previous_sibling().get_text().replace('zł', '').strip().replace(' ','')),
                        'status':'no-info'
                    })


            nextPage=soup.find('a', title='następna')

            if nextPage is not None:
                response=requests.get(url+nextPage['href'])
                soup=BeautifulSoup(response.text, "html.parser")
                flats=soup.tbody.find_all('tr')
            else:
                break
        flatsList.append(temporaryList)
        sumUp.append(summarize(temporaryList))

    return flatsList, sumUp

