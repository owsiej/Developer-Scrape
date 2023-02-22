from collections import Counter


def standardize_status(status: str):

    statusNamesSold=['sprzedane', 'sold']
    statusNamesFree=['dostępne', 'free', 'wolne', 'available']
    statusNamesReserved=['rezerwacja', 'reserved']

    if status.lower() in statusNamesSold:
        return 'sprzedane'
    if status.lower() in statusNamesFree:
        return 'wolne'
    if status.lower() in statusNamesReserved:
        return 'zarezerwowane'
    else:
        return 'no-info'

def standardize_floor_number(number):
    if number.lower()=='parter':
        return 0
    if 'i' in number.lower().strip(' '):
        return 1
    if 'ii' in number.lower().strip(' '):
        return 2
    if 'iii' in number.lower().strip(' '):
        return 3
    if 'iv' in number.lower().strip(' '):
        return 4
    if 'v' in number.lower().strip(' '):
        return 5
    if 'vi' in number.lower().strip(' '):
        return 6
    else:
        return number
    
def str_to_float(numb):
    if numb=='':
        return 'no-info'
    return float(numb)

def summarize(lista:list):

    counter=Counter(map(lambda item: item['status'], lista))

    pricesForSQM=[round(flat['price']/flat['area'],2)
                  for flat in lista
                  if isinstance(flat['price'], (float, int)) and isinstance(flat['area'], (float, int))]

    investSumUp={lista[0]['flat_name']:{'amount_of_all_flats':int(len(lista)),                                  'amount_of_sold_flats':counter['sprzedane'],
                                  'amount_of_free_flats':int(counter['wolne']),
                                  'amount_of_reserved_flats':int(counter['zarezerwowane']),
                                  'amount_of_no-info_flats':int(counter['no-info']),
                                  'minimum_price_for_m2':min(pricesForSQM) if pricesForSQM else 0,
                                  'maximum_price_for_m2':max(pricesForSQM) if pricesForSQM else 0}
    }
    return investSumUp