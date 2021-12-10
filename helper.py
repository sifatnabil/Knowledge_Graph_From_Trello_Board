import requests
from env import key, token
from pprint import pprint

# * Get members of a board  
def get_board_members(board_id):
    url = f'https://api.trello.com/1/boards/{board_id}/members?key={key}&token={token}'
    response = requests.get(url)
    return response.json()

# * Get members of a card
def get_card_members(card_id):
    url = f'https://api.trello.com/1/cards/{card_id}/members?key={key}&token={token}'
    response = requests.get(url)
    return response.json()
    
# * Create members of a board as tuple
def get_board_members_tupl_ls(members):
    members_tupl = []
    for member in members:
        members_tupl.append((member['id'], member['fullName'].lower(), member['username']))
    return members_tupl

# * Get all the cards of one board
def get_cards(board_id):
    url = f'https://api.trello.com/1/boards/{board_id}/cards?key={key}&token={token}'
    response = requests.get(url)
    return response.json()

# * Create Tuple of cards
def get_cards_tupl_ls(cards):
    cards_tupl = []
    for card in cards:
        cards_tupl.append((card['id'], card['name'].lower(), card['desc'], card['shortUrl']))
    return cards_tupl

# * Get the name of the board
def get_board_name(board_id):
    url = f'https://api.trello.com/1/boards/{board_id}?key={key}&token={token}'
    response = requests.get(url)
    return response.json()['name']

# * Get all the checklists of each card
def get_checklists(board_id):
    url = f'https://api.trello.com/1/boards/{board_id}/checklists?key={key}&token={token}'
    response = requests.get(url)
    return response.json()

# * Create Checklists Tuple
def get_checklists_tupl_ls(checklists):
    checklists_tupl = []
    for checklist in checklists:
        check_items = checklist['checkItems']
        for item in check_items:
            checklists_tupl.append((checklist['id'], item['name'].lower(), item['state']))
    return checklists_tupl

# * Get checklists of card
def get_card_checklists(card_id):
    url = f'https://api.trello.com/1/cards/{card_id}/checklists?key={key}&token={token}'
    response = requests.get(url)
    return response.json()

# * Get cards with checklists
def get_cards_with_checklists(cards):
    cards_with_checklists = []
    for card in cards:
        card_id, name, url = card['id'], card['name'].lower(), card['shortUrl']
        checklists = get_card_checklists(card_id)
        checklist_ls = []
        for checklist in checklists:
            check_items = checklist['checkItems']
            for item in check_items:
                checklist_ls.append({
                    "name": item['name'].lower(),
                    "state": item['state'],
                })
        cards_with_checklists.append({
            "id": card_id,
            "name": name.lower(),
            "url": url,
            "checklists": checklist_ls,
        })
    return cards_with_checklists
