from bs4 import BeautifulSoup
import requests
from standardize_flat_info import summarize



def get_flats_info():
    """get infos of all flats

    Args:
        all_buildings (list): list of all buildings with ids used in api

    Returns:
        list with infos of all flats developer has got
    """
    floor_count=1
    buildings=[{'name': 'Apartamenty Jagiellońskie etap V',
                'link': f'https://apartamentyjagiellonskie.pl/pietro-{floor_count}',
                'stage': 'etap V'},
               {'name': 'Apartamenty Jagiellońskie etap VI',
                'link': f'https://apartamentyjagiellonskie.pl/pietro-{floor_count}-2',
                'stage': 'etap VI'}]

    flatsList=[]
    sumUp=[]

    for building in buildings:
        temporaryList=[]
        for floor_count in range(1,11):

            params={
                    'szukaj':'true',
                    'budynek':building['stage'],
                    'pietro':floor_count
                }
            response=requests.get(f"{building['link']}", params)
            soup=BeautifulSoup(response.text, "html.parser")
            flats=soup.tbody.find_all('tr')[1:]
            
            
            for flat in flats:
                temporaryList.append({
                    'flat_name':building['name'],
                    'floor_number':flat.find(attrs={'data-th':'Piętro'}).get_text().strip().split()[1],
                    'rooms_number':flat.find(attrs={'data-th':'Liczba pokoi'}).get_text().strip(),
                    'area':float(flat.find(attrs={'data-th':'Metraż'}).get_text().replace('m2', '').strip()),
                    'price':'no-info',
                    'status':flat.find(attrs={'data-th':'Status'}).get_text().strip(),
                })
        flatsList.append(temporaryList)
        sumUp.append(summarize(temporaryList))
        
    return flatsList, sumUp





