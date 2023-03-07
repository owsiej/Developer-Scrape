from models import FlatModel
import re


def set_operator_and_key(word) -> list:
    pattern = re.compile(r"(__lt$|__gt$)")
    match = pattern.search(word)

    if match:
        if match.group() == '__lt':
            return [word.replace(match.group(), ''), '<']

        elif match.group() == '__gt':
            return [word.replace(match.group(), ''), '>']

    return [word, '=']


def find_filters(query_params):
    critters = [
        {
            'arg': set_operator_and_key(key)[0],
            'operator': set_operator_and_key(key)[1],
            'value': value
        }
        for key, value in query_params.items()
    ]
    filters = []
    for critter in critters:
        if critter['arg'] == 'floor_number':
            if critter['operator'] == '>':
                filters.append(FlatModel.floor_number > critter['value'])
            if critter['operator'] == '<':
                filters.append(FlatModel.floor_number < critter['value'])
            if critter['operator'] == '=':
                filters.append(FlatModel.floor_number == critter['value'])
        if critter['arg'] == 'rooms_number':
            if critter['operator'] == '>':
                filters.append(FlatModel.rooms_number > critter['value'])
            if critter['operator'] == '<':
                filters.append(FlatModel.rooms_number < critter['value'])
            if critter['operator'] == '=':
                filters.append(FlatModel.rooms_number == critter['value'])
        if critter['arg'] == 'area':
            if critter['operator'] == '>':
                filters.append(FlatModel.area > critter['value'])
            if critter['operator'] == '<':
                filters.append(FlatModel.area < critter['value'])
            if critter['operator'] == '=':
                filters.append(FlatModel.area == critter['value'])
        if critter['arg'] == 'price':
            if critter['operator'] == '>':
                filters.append(FlatModel.price > critter['value'])
            if critter['operator'] == '<':
                filters.append(FlatModel.price < critter['value'])
            if critter['operator'] == '=':
                filters.append(FlatModel.price == critter['value'])
        if critter['arg'] == 'status':
            if critter['operator'] == '=':
                filters.append(FlatModel.status == critter['value'])

    return filters
