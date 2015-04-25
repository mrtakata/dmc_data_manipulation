__author__ = 'matheustakata'

import json
import re
import urllib2

"""
    Gets Deadman's Cross card data from dccards.io and
    saves locally on a file called cards.json
"""
def get_data_from_api():
    url = 'http://api.dccards.io/GetAllCards/Pretty/'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = response.read()
    json_file = open("cards.json", 'r+')
    json_file.write(data)
    json_file.close()

"""
    Returns a dictionary with all limited cards (Virulents and Pestilents)
    The key of each object is the name of the card.
"""
def get_limited_cards():
    limited_cards = {}
    for card in json_cards:
        if card['Rarity'] == "Virulent" or card['Rarity'] == "Pestilent":
            limited_cards[card['Name']] = card

    return limited_cards

"""
    Returns a dictionary with all Legendary cards (5-star non-limited cards)
    The key of each object is the name of the card.
"""
def get_legendary_cards():
    legendary_cards = {}
    for card in json_cards:
        if card['Rarity'] == "Legendary":
            legendary_cards[card['Name']] = card
    return legendary_cards

"""
    Returns a dictionary with all 5-star cards
    The key of each object is the name of the card.
"""
def get_all_five_stars():
    all_five_stars = get_legendary_cards().copy()
    all_five_stars.update(get_limited_cards())
    return all_five_stars

"""
    Inputs: list: dict, stat: string
    Returns an array with the keys of the list sorted by the stat
"""
def print_sorted_by(list, stat):
    sorted_list ={}
    sorted_list = sorted(list, key=lambda x:list[x]['AverageStats'].get(stat), reverse = True)
    for card in sorted_list:
        print (str(list[card]['Name']) + ', ' + stat + ': ' + "%.0f" % float(max_stat_boosted(list[card],stat)))

"""
    Input: card_name: string
    Returns the card data wanted
"""
def get_card(card_name):
    for card in json_cards:
        if card['Name'] == card_name:
            return card
    return 'Error: card not found'

"""
    Inputs: card_name: string, stat: string, max_or_min: string
    Returns the card min or max stat wanted
"""
def get_card_stat(card_name, stat, max_or_min):
    if max_or_min.upper() == 'MAX':
        return get_card(card_name)['AverageStats'][stat]['Max']
    elif max_or_min.upper() == 'MIN':
        return get_card(card_name)['AverageStats'][stat]['Min']
    return 'Error: wrong use of the function'

"""
    The following functions are related to the calculation of a card stat
"""

"""
    Returns the amount of points a card get on a stat when leveling up
"""

def stat_per_level(card, stat):
    return (float(card['AverageStats'][stat]['Max'] - card['AverageStats'][stat]['Min']) / (card['MaxLevel']-1))

"""
    Returns max stat after the redeath of a given card
"""
def max_stat_redeathed(card, stat):
    if card['Rarity'] == 'Legendary' or card['Rarity'] == "Virulent" or card['Rarity'] == "Pestilent":
        return card['AverageStats'][stat]['Max'] + 10 * stat_per_level(card, stat)
    elif card['Rarity'] == 'Epic' or card['Rarity'] == 'Epic Plus':
        return card['AverageStats'][stat]['Max'] + 5 * stat_per_level(card, stat)
    return "Card not found or not redeathable"
"""
    Returns boost points of a stat
"""
def boost_points(card, stat):
    return card['AverageStats'][stat]['Max'] / 5.0

"""
    Returns boost points after redeath of a stat
"""
def boost_points_redeathed(card, stat):
    return max_stat_redeathed(card, stat) * 0.2

"""
    Returns the max points a card can have on a given stat after redeathing and boosting
"""
def max_stat_boosted(card, stat):
    return max_stat_redeathed(card, stat) + boost_points_redeathed(card, stat)


def get_card_buff_abilities(card):
    card_buffs = []
    for ability in card['Abilities']:
        if re.match('(A|D|S|I|R){1,2}\d{2}.*(Mutation|Metabolism|Metastasis)', str(card['Abilities'][ability])):
            card_buffs.append(card['Abilities'][ability])
    return card_buffs

def buff_stats(card):
    stats = {
        "Attack": max_stat_boosted(card, "Attack"),
        "Defense": max_stat_boosted(card, "Defense"),
        "Speed": max_stat_boosted(card, "Speed"),
        "Intelligence": max_stat_boosted(card, "Intelligence")
    }
    card_buffs = get_card_buff_abilities(card)
    for buff in card_buffs:
        if buff[0] == 'A' and re.match('\d', buff[1]):
            stats["Attack"] = stats["Attack"]* float('1.'+buff[1:3])
        if buff[0] == 'D' and re.match('\d', buff[1]):
            stats["Defense"] = stats["Defense"]* float('1.'+buff[1:3])
        if buff[0] == 'S' and re.match('\d', buff[1]):
            stats["Speed"] = stats["Speed"]* float('1.'+buff[1:3])
        if buff[0] == 'I' and re.match('\d', buff[1]):
            stats["Intelligence"] = stats["Intelligence"] * float('1.'+buff[1:3])

        if buff[0:2] =='AD':
            stats["Attack"] = stats["Attack"]* float('1.'+buff[2:4])
            stats["Defense"] = stats["Defense"]* float('1.'+buff[2:4])
        if buff[0:2] =='AS':
            stats["Attack"] = stats["Attack"]* float('1.'+buff[2:4])
            stats["Speed"] = stats["Speed"]* float('1.'+buff[2:4])
        if buff[0:2] =='AI':
            stats["Attack"] = stats["Attack"]* float('1.'+buff[2:4])
            stats["Intelligence"] = stats["Intelligence"] * float('1.'+buff[2:4])
        if buff[0:2] =='DS':
            stats["Defense"] = stats["Defense"]* float('1.'+buff[2:4])
            stats["Speed"] = stats["Speed"]* float('1.'+buff[2:4])
        if buff[0:2] =='DI':
            stats["Defense"] = stats["Defense"]* float('1.'+buff[2:4])
            stats["Intelligence"] = stats["Intelligence"] * float('1.'+buff[2:4])
        if buff[0:2] =='SI':
            stats["Speed"] = stats["Speed"]* float('1.'+buff[2:4])
            stats["Intelligence"] = stats["Intelligence"] * float('1.'+buff[2:4])
    return stats

all_stats = ["Health", "Psyche", "Attack", "Defense", "Speed", "Intelligence"]
#loads data into the program
json_file = open("cards.json")
json_data = json_file.read()
json_data = json.loads(json_data)
json_cards = json_data['info']
json_file.close()