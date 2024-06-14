import requests
from typing import List, Dict, Any
from application.models import CardInfo
from application import db
from run import app

def fetch_scryfall_cards() -> List[Dict[str, Any]]:
    '''Fetches the default cards from Scryfall'''
    print('Fetching cards from Scryfall...')
    bulk_data_url = 'https://api.scryfall.com/bulk-data'
    bulk_data_response = requests.get(bulk_data_url)
    bulk_data_response.raise_for_status()
    bulk_data = bulk_data_response.json()

    default_cards_data = next(item for item in bulk_data['data'] if item['type'] == 'default_cards')
    default_cards_url = default_cards_data['download_uri']

    resp = requests.get(default_cards_url)
    resp.raise_for_status()
    return resp.json()

def extract_card_info(scryfall_data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    card_info = {}
    unhandled_layouts = set()

    for card in scryfall_data:
        name = card.get('name', '').upper().strip()
        layout = card.get('layout')

        if layout in ['transform', 'split', 'flip', 'adventure', 'modal_dfc', 'reversible_card']:
            faces = card.get('card_faces', [])
            if faces:
                main_face = faces[0]
                name = main_face.get('name', '').upper().strip()
                mana_cost = main_face.get('mana_cost', '').replace('//', '').replace(' ', '')
                type_line = main_face.get('type_line', '')
                image = main_face.get('image_uris', {}).get('normal', '')

                if layout == 'split':
                    secondary_face = faces[1]
                    mana_cost += secondary_face.get('mana_cost', '').replace('//', '').replace(' ', '')

                card_info[name] = {
                    'mana_cost': mana_cost,
                    'type_line': type_line,
                    'image': image  # Added missing comma
                }
        else:
            mana_cost = card.get('mana_cost', '')
            type_line = card.get('type_line', '')
            image = card.get('image_uris', {}).get('normal', '')

            if name not in card_info:
                card_info[name] = {
                    'mana_cost': mana_cost,
                    'type_line': type_line,
                    'image': image  # Added missing comma
                }
            else:
                unhandled_layouts.add(layout)

    for layout in unhandled_layouts:
        print(f"Unhandled layout: {layout}")

    return card_info

def store_card_info(card_info: Dict[str, Dict[str, Any]]):

    for name, info in card_info.items():
        card = CardInfo(
            card_name=name,
            mana_cost=info['mana_cost'],
            type_line=info['type_line'],
            image=info['image']
        )
        db.session.add(card)

    db.session.commit()
    db.session.close()


if __name__ == "__main__":
    with app.app_context():
        scryfall_data = fetch_scryfall_cards()
        card_info = extract_card_info(scryfall_data)
        store_card_info(card_info)
