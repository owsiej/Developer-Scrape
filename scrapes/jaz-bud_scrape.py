from services.scrape_logic.scrape_functions import get_developer_info, get_developer_investments, get_new_page_links, \
    get_investment_flats

developerName = 'Jaz-Bud'

baseUrl = 'https://www.jaz-bud.pl'
cityTag = '/bialystok'

investmentHtmlInfo = {'investmentTag': ".find('ul', class_='uk-nav uk-navbar-dropdown-nav').find_all('li')",
                      'investmentName': ".get_text()",
                      'investmentLink': ".a['href']"}
investmentsInfo = get_developer_investments(baseUrl, investmentHtmlInfo)

newPageHtmlPage = {'nextPageTag': ".find('a', title='następna')",
                   'nextPageLink': "['href']"}

investmentsFinalInfo = get_new_page_links(investmentsInfo, newPageHtmlPage, baseUrl)
flatsHtmlInfo = {'flatTag': ".tbody.find_all('tr')",
                 'floorNumber': ".find('td', {'data-order':re.compile('^piętro')}).span.get_text(strip=True) if flat.find('td', {'data-order':re.compile('^piętro')}) else None",
                 'roomsAmount': ".find('td', {'data-order':re.compile('^pokoje')}).span.get_text(strip=True)  if flat.find('td', {'data-order':re.compile('^pokoje')}) else None",
                 'area': ".find('td', {'data-order':re.compile('^powierzchnia')}).span.get_text(strip=True).replace('m2','')  if flat.find('td', {'data-order':re.compile('^powierzchnia')}) else None",
                 'price': ".find('td', {'data-order':re.compile('^[0-9]')}).div.get_text(strip=True).replace('zł', '') if flat.find('td', {'data-order':re.compile('^[0-9]')}) else None",
                 'status': ""}
#
developerData = get_developer_info(developerName, baseUrl)

investmentsData = list(map(lambda item: {
    'name': item['name'],
    'url': baseUrl + item['url']
}, investmentsInfo))

flatsData = get_investment_flats(investmentsFinalInfo, flatsHtmlInfo, baseUrl)

for flat in flatsData:
    print(flat)
