from bs4 import BeautifulSoup
import requests
from standardize_flat_info import standardize_status, standardize_floor_number


def get_developer_info(name: str, url: str) -> dict:
    """

    Args:
        name: Name of developer
        url: Take link to developer page

    Returns:
        Object - developer name, url

    """
    developer = {"name": name,
                 "link": url}
    return developer


def get_developer_investments(url, htmlData: dict) -> list:
    """

    Args:
        url: link to developer page
        htmlData: dictionary with strings of code for:
         investmentTag - tag in html where new investment is added
         investmentName - tag containing investment name
         investmentLink - tag containing link to investment
    Returns:
        Object - Investment name, link to investment
    """
    developerInvestments = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data = eval(f"soup.{htmlData['investmentTag']}")

    for item in data:
        developerInvestments.append({"name": eval(f"item.{htmlData['investmentName']}"),
                                     "link": eval(f"item.{htmlData['investmentLink']}")})

    return developerInvestments


def get_investment_flats(investmentInfo: list, htmlData: dict) -> list:
    """

    Args:
        investmentInfo: list with infos about investment (return of get_developer_investments)
        htmlData: dictionary with strings of code for:
         flatTag - tag in html where new flat is added
         floorNumber - tag containing floor number of flat,
         roomsAmount - tag containing rooms number of flat,
         area - tag containing area of flat,
         price - tag containing price of flat,
         status - tag containing status of flat
    Returns:
        list of dictionaries containing all info about flat
    """
    flats = []

    for investment in investmentInfo:
        response = requests.get(f"{investment['link']}")
        soup = BeautifulSoup(response.text, "html.parser")
        data = eval(f"soup.{htmlData['flatTag']}")

        for flat in data:
            flats.append({
                'flat_name': investment['name'],
                'floor_number': standardize_floor_number(eval(f"flat.{htmlData['floorNumber']}")),
                'rooms_number': eval(f"flat.{htmlData['roomsAmount']}"),
                'area': eval(f"flat.{htmlData['area']}") if htmlData['area'] else 'no-info',
                'price': eval(f"flat.{htmlData['price']}") if htmlData['price'] else 'no-info',
                'status': standardize_status(eval(f"flat.{htmlData['status']}"))
            })
    return flats
