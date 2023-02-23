from bs4 import BeautifulSoup
import requests
from standardize_flat_info import standardize_status, standardize_floor_number, summarize

baseUrls = {'Apartamenty Sienkiewicza': 'https://www.birkbud.pl/apartamentysienkiewicza/',
            'Złote Kaskady': 'https://www.birkbud.pl/zlotekaskady/',
            'Rzemieślnicza': 'https://www.birkbud.pl/rzemieslnicza13/'}


def get_flats_info(urls=baseUrls):
    flatsList = []
    sumUp = []

    for url in list(urls.values()):

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        flats = soup.tbody.find_all('tr')
        temporaryList = []
        for flat in flats:
            temporaryList.append({
                'flat_name':
                    soup.article.find('h2', class_='elementor-heading-title elementor-size-default').get_text().replace(
                        '"', '').split(',')[0],
                'floor_number': standardize_floor_number(flat.find(class_='column-1').get_text()),
                'rooms_number': flat.find(class_='column-4').get_text(),
                'area': float(flat.find(class_='column-3').get_text().replace('m²', '').replace(',', '.').strip()),
                'price': 'no-info',
                'status': standardize_status(flat.find(class_='column-8').get_text().strip())
            })
        flatsList.append(temporaryList)
        sumUp.append(summarize(temporaryList))
    return flatsList, sumUp


response = requests.get('https://www.birkbud.pl/nieruchomosci/')
soup = BeautifulSoup(response.text, "html.parser")
invests = soup.find_all('section', {'data-element_type': 'section'})
print(invests)
print(len(invests))
