from itertools import chain
from scrape_functions import get_developer_info, get_investment_flats

developerName = 'Apartamenty Jagiellońskie'
baseUrl = 'https://apartamentyjagiellonskie.pl/'

investmentsInfo = list(chain.from_iterable([[{'name': "Apartamenty Jagiellońskie etap V",
                                              'link': f"https://apartamentyjagiellonskie.pl/pietro-{floor_count}"
                                                      f"/?szukaj=true&budynek=etap%20V&pietro={floor_count}"}
                                             for floor_count in range(1, 11)],
                                            [{'name': "Apartamenty Jagiellońskie etap VI",
                                              'link': f"https://apartamentyjagiellonskie.pl/pietro-{floor_count}-2"
                                                      f"/?szukaj=true&budynek=etap%20VI&pietro={floor_count}"}
                                             for floor_count in range(1, 11)]]))

flatsHtmlInfo = {'flatTag': ".tbody.find_all('tr')[1:]",
                 'floorNumber': ".find(attrs={'data-th':'Piętro'}).get_text().strip().split()[1]",
                 'roomsAmount': ".find(attrs={'data-th':'Liczba pokoi'}).get_text().strip()",
                 'area': ".find(attrs={'data-th':'Metraż'}).get_text().replace('m2', '').strip()",
                 'price': "",
                 'status': ".find(attrs={'data-th':'Status'}).get_text().strip()"}

developerData = get_developer_info(developerName, baseUrl)

investmentsData = [investmentsInfo[0], investmentsInfo[10]]

flatsData = get_investment_flats(investmentsInfo, flatsHtmlInfo)
