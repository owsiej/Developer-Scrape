from itertools import chain
import time
from services.scrape_logic.scrape_functions import get_developer_info, get_developer_investments, \
    get_all_buildings_from_investment, get_investment_flats_from_api

developerName = 'Rogowski Development'
baseUrl = 'https://www.rogowskidevelopment.pl/'

investmentHtmlInfo = {
    'investmentTag': ".find(class_='home-boxes no-gutter row').find_all('a', attrs={'title':re.compile(r'Białystok$')})",
    'investmentName': "['title'].split(',')[0]",
    'investmentLink': "['href']"}

allBuildingsInInvestmentsHtmlInfo = {
    'investmentTag': ".select('[data-id]')",
    'investmentName': ".get_text()",
    'investmentLink': "['href']"
}

investmentBuildingsIdsHtmlInfo = {'buildingTag': ".select('[data-id]')",
                                  'buildingName': "['name']",
                                  'buildingLink': "['data-id']"}

flatsHtmlInfo = {'floorNumber': "['floor_number'][0]['floor_number']",
                 'roomsAmount': "['rooms']",
                 'area': "['sqm']",
                 'price': "['price']",
                 'status': "['state'][0]"}

investmentsLinks = get_developer_investments(baseUrl, investmentHtmlInfo)

allBuildingsInInvestments = list(chain.from_iterable([
    get_developer_investments(item['url'], allBuildingsInInvestmentsHtmlInfo)
    for item in investmentsLinks
]))

investmentsIds = get_all_buildings_from_investment(allBuildingsInInvestments, investmentBuildingsIdsHtmlInfo)

investmentsInfo = [{
    'name': invest['name'],
    'url': "https://www.rogowskidevelopment.pl/wp-json/wp/v2/flat?filter[meta_key_value_compare]"
           f"[stage][{invest['url']}]==&filter[meta_key_value_compare][object_type]"
           f"[flat]==&filter[meta_key_value_compare][state][inactive]=!=&filter[posts_per_page]=-1"}
    for invest in investmentsIds]

developerData = get_developer_info(developerName, baseUrl)

investmentsData = allBuildingsInInvestments
start_time = time.time()

flatsData = get_investment_flats_from_api(investmentsInfo, flatsHtmlInfo)
print(f"{(time.time() - start_time):.2f}")
