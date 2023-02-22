import requests
from standardize_flat_info import standardize_status, summarize

urlApi='https://rutkowskidevelopment.pl/wp-content/themes/hubdab_starter/api.json'


def get_flats_info(url=urlApi):

    response=requests.get(url)

    r=response.json()

    flatsList=[]
    investmentsNames=set()
    sumUp=[]
    for flat in r['lokale']:
        if flat['miasto']=='Białystok' and flat['typ']=='Mieszkanie':
            investmentsNames.add(flat['osiedle'])
            flatsList.append({
                    'flat_name':flat['osiedle'],
                    'floor_number':flat['pietro'],
                    'rooms_number':flat['liczba_pokoi'],
                    'area':flat['powierzchnia'],
                    'price':'no-info',
                    'status':standardize_status(flat['status'])
                })
    flatsList.sort(key= lambda item: (item['flat_name'], item['floor_number']))

    for name in list(investmentsNames):
        temporaryList=[]
        for flat in flatsList:
            if flat['flat_name']==name:
                temporaryList.append(flat)
        sumUp.append(summarize(temporaryList))
    
    return [flatsList], sumUp