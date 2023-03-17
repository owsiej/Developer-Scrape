from services.scrape_logic.scrape_functions import get_developer_info, get_developer_investments, get_new_page_links, \
    get_investment_flats

developerName = 'Jaz-Bud'

baseUrl = 'https://www.jaz-bud.pl'
cityTag = '/bialystok'

investmentHtmlInfo = {'investmentTag': ".find('ul', class_='nav-child')",
                      'investmentName': ".get_text()",
                      'investmentLink': ".a['href']"}
investmentsInfo = get_developer_investments(baseUrl, investmentHtmlInfo)

newPageHtmlPage = {'nextPageTag': ".find('a', title='następna')",
                   'nextPageLink': "['href']"}

investmentsFinalInfo = get_new_page_links(investmentsInfo, newPageHtmlPage, baseUrl)

flatsHtmlInfo = {'flatTag': ".tbody.find_all('tr')",
                 'floorNumber': ".find(class_='fa fa-search').find_parent().find_parent()"
                                ".find_previous_sibling().find_previous_sibling().find_previous_sibling().get_text()",
                 'roomsAmount': ".find(class_='fa fa-search').find_parent().find_parent()"
                                ".find_previous_sibling().find_previous_sibling().get_text()",
                 'area': ".find(class_='fa fa-search').find_parent().find_parent().find_previous_sibling()"
                         ".find_previous_sibling().find_previous_sibling().find_previous_sibling().get_text()"
                         ".replace('m2', '').replace(',', '.').strip()",
                 'price': ".find(class_='fa fa-search').find_parent().find_parent()"
                          ".find_previous_sibling().get_text().replace('zł', '').strip().replace(' ','')",
                 'status': ""}

developerData = get_developer_info(developerName, baseUrl)

investmentsData = list(map(lambda item: {
    'name': item['name'],
    'url': baseUrl + item['url']
}, investmentsInfo))

flatsData = get_investment_flats(investmentsFinalInfo, flatsHtmlInfo, baseUrl)
