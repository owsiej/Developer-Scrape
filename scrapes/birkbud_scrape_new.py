from scrape_functions import get_developer_info, get_investment_flats

developerName = 'Birkbud'
baseUrl = 'https://www.birkbud.pl/nieruchomosci/'

investmentsInfo = [{'name': 'Apartamenty Sienkiewicza', 'link': 'https://www.birkbud.pl/apartamentysienkiewicza/'},
                   {'name': 'Złote Kaskady', 'link': 'https://www.birkbud.pl/zlotekaskady/'},
                   {'name': 'Rzemieślnicza', 'link': 'https://www.birkbud.pl/rzemieslnicza13/'}]

flatsHtmlInfo = {'flatTag': "tbody.find_all('tr')",
                 'floorNumber': "find(class_='column-1').get_text()",
                 'roomsAmount': "find(class_='column-4').get_text()",
                 'area': "find(class_='column-3').get_text().replace('m²', '').replace(',', '.').strip()",
                 'price': '',
                 'status': "find(class_='column-8').get_text().strip()"}

developerInfo = get_developer_info(developerName, baseUrl)

flatsInfo = get_investment_flats(investmentsInfo, flatsHtmlInfo)

print(developerInfo)
for flat in flatsInfo:
    print(flat)

investmentsInfo_2 = [{'name': 'Inwestycja Andruszkiewicza', 'link': 'https://www.birkbud.pl/andrukiewicza/'}]

flatsHtmlInfo_2 = {'flatTag': "tbody.find_all('tr')",
                   'floorNumber': "find(class_='column-1').get_text()",
                   'roomsAmount': "find(class_='column-6').get_text()",
                   'area': "find(class_='column-4').get_text().replace('m²', '').replace(',', '.').strip()",
                   'price': '',
                   'status': "find(class_='column-8').get_text().strip()"}

flatsInfo = get_investment_flats(investmentsInfo_2, flatsHtmlInfo_2)

for flat in flatsInfo:
    print(flat)
