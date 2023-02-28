from scrape_functions import get_developer_info, get_developer_investments, get_investment_flats

developerName = 'Asko S.A.'
baseUrl = 'https://askosa.pl/inwestycja'

investmentHtmlInfo = {'investmentTag': "find_all(class_='properties__info')",
                      'investmentName': "find(class_='properties__address-street').get_text()",
                      'investmentLink': "a['href']"}

flatsHtmlInfo = {'flatTag': "tbody.find_all('tr')",
                 'floorNumber': "td.find_next_sibling().find_next_sibling().find_next_sibling().get_text()",
                 'roomsAmount': "td.find_next_sibling().find_next_sibling().get_text()",
                 'area': "td.find_next_sibling().get_text().replace('m2', '').strip()",
                 'price': """td.find_next_sibling().find_next_sibling().find_next_sibling()\
.find_next_sibling().find_next_sibling().find_next_sibling().get_text().replace('zł', '')\
.replace(' ', '').strip()""",
                 'status': """td.find_next_sibling().find_next_sibling().find_next_sibling()\
.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()"""}

developerInfo = get_developer_info(developerName, baseUrl)

investmentsInfo = get_developer_investments(baseUrl, investmentHtmlInfo)

flatsInfo = get_investment_flats(investmentsInfo, flatsHtmlInfo)

print(developerInfo)
print(investmentsInfo)
for flat in flatsInfo:
    print(flat)
