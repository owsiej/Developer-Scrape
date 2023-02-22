import requests
from standardize_flat_info import standardize_status, str_to_float, summarize

apiUrl='http://panoramabialystok.pl/wp-admin/admin-ajax.php' \
'?action=wp_ajax_ninja_tables_public_action&table_id=912' \
'&target_action=get-all-data&default_sorting=manual_sort'

def get_flats_info(url=apiUrl):

    response=requests.get(url)
    r=response.json()
    flatsList=[]
    
    for flat in r:
        flatsList.append({
        'flat_name':'Panorama Park',
        'floor_number':flat['value']['545'],
        'rooms_number':flat['value']['pokoje'],
        'area':float(flat['value']['powierzchnia'].replace('mkw.', '').strip().replace(',', '.')),
        'price':str_to_float(flat['value']['cena']),
        'status':standardize_status(flat['value']['status'])
    })
    sumUp=[summarize(flatsList)]
    return [flatsList], sumUp





