from scrape_functions import get_developer_info, get_developer_investments, get_investment_flats_from_api_condition

developerName = 'Constrim '
baseUrl = 'https://constrim.pl/'
apiUrls = [
    'https://smart-makieta-3destate-embed.azureedge.net/assets/5b306c4f-895e-434b-9913-c70550fc4f73/app.config.json',
    'https://smart-makieta-3destate-embed.azureedge.net/assets/6a56c6d7-ba7f-4348-a4c9-951768b7ef72/app.config.json']

investmentHtmlInfo = {
    'investmentTag': ".find('ul', class_='sub-menu').find_all('a')",
    'investmentName': ".get_text()",
    'investmentLink': "['href']"}

investmentsInfo = get_developer_investments(baseUrl, investmentHtmlInfo)

investmentsApiInfo = [{
    'name': name['name'],
    'link': link}
    for name, link in zip(investmentsInfo, apiUrls)]

flatsHtmlInfo = {'dataLocation': "['flats']",
                 'dataCondition': "flat['custom']['type']=='apartment'",
                 'floorNumber': "['floor']",
                 'roomsAmount': "['rooms']",
                 'area': "['area']",
                 'price': "",
                 'status': "['availability']"}

developerData = get_developer_info(developerName, baseUrl)

investmentsData = investmentsInfo

flatsData = get_investment_flats_from_api_condition(investmentsApiInfo, flatsHtmlInfo)
