from bs4 import BeautifulSoup
import requests
import unicodedata
from standardize_flat_info import standardize_status, summarize

baseUrl='https://www.kombinatbud.com.pl'
baseTag='/Inwestycje'

response=requests.get(f'{baseUrl}{baseTag}')
startSoup=BeautifulSoup(response.text, "html.parser")


def decode_string(string):
    return unicodedata.normalize('NFKD', string)

def check_reservation(fl):
    try:
        if fl['title']:
            return 'reserved'
    except KeyError:
        return 'free'

def unpack_nested_list(array: list):
    unpackedList=[]
    for item in array:
        if isinstance(item, list):
            for piece in item:
                unpackedList.append(piece)
        else:
            unpackedList.append(item)
    return unpackedList


def get_all_developer_invests(scrape: BeautifulSoup):
    """# get names of all investments and links to them from front page
    Args:
        scrape (BeautifulSoup): object ready to scrape

    Returns:
        all investments of developer in list
    """
    result=[]

    investments=scrape.find_all(class_='covers')[0].find_all('a')
    for invest in investments:
        result.append({
            'name':decode_string(invest.find('h3').get_text()),
            'link':invest['href']
        })
    return result

def get_all_buildings(url=baseUrl):
    """get names of all investments with links to them

    Args:
        investments (list): investments from which we gonna get buildings
    Returns:
        list of whole need data
    """
    investments=get_all_developer_invests(startSoup)
    listOfBuildings=[]
    
    for investment in investments:


        response2=requests.get(f"{url}{investment['link']}")
        soup2=BeautifulSoup(response2.text, "html.parser")

        buildings=soup2.find_all(class_='button-wrapper')
        links=[building.find(class_='button w-100')['href']
            for building in buildings
            if building.find(class_='button w-100')['href']!='#']
        if links:   
            listOfBuildings.append({'name':investment['name'],
                                        'link':links})
        else:
            listOfBuildings.append(investment)
        
    return listOfBuildings


def get_flats_info(url=baseUrl):
    """get infos of all flats

    Args:
        all_buildings (list): list of all buildings with ids used in api

    Returns:
        list with infos of all flats developer has got
    """
    buildings=get_all_buildings()
    flatsList=[]
    sumUp=[]

    allLinks=unpack_nested_list([invest['link']
            for invest in buildings])

    for link in allLinks:

        response3=requests.get(f"{url}{link}")
        soup3=BeautifulSoup(response3.text, "html.parser")

        try:
            nameSoup=BeautifulSoup(response3.text, "html.parser")
            name=nameSoup.find(class_='h5').next_sibling.get_text().strip()
            flats=soup3.tbody.select('tr')

        except AttributeError:
            pass
        else:
            temporaryList=[]
            for flat in flats:
                prices=flat.find(class_='text-danger')
                if prices:
                    price=decode_string(prices.find_next_sibling('b').get_text())
                else:
                    price=decode_string(flat.find(class_='desktop').find_next_sibling().find_next_sibling().find_next_sibling().get_text())
                temporaryList.append({
                    'flat_name':name,
                    'floor_number':decode_string(flat.find(class_='desktop').get_text()),
                    'rooms_number':int(decode_string(flat.find(class_='desktop').find_next_sibling().get_text())),
                    'area':float(decode_string(flat.find(class_='desktop').find_next_sibling().find_next_sibling().get_text()).replace(' m2', '').replace(',', '.')),
                    'price':int(price.replace('PLN', '').replace(' ', '').strip()),
                    'status': standardize_status(check_reservation(flat))
                    })
            flatsList.append(temporaryList)
            sumUp.append(summarize(temporaryList))
    return flatsList, sumUp



# allInvestments=get_all_developer_invests(soup)
# allBuildings=get_all_buildings(allInvestments, baseUrl)
# allFlatsInBuildings,summarizedFlatsInfos=get_flats_info(allBuildings, baseUrl)



