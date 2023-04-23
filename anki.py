import os
import random
import json
import genanki
import requests

# Set up the AnkiConnect API endpoint
url = "http://localhost:8765"
headers = {
    "Content-Type": "application/json",
}

# Read flashcards from JSON files
flashcards_by_file = {}
for file_name in os.listdir('out_json'):
    if file_name.endswith('.json') and not file_name.endswith('.bck.json'):
        with open(f'out_json/{file_name}', 'r') as f:
            flashcards = json.load(f)
        flashcards_by_file[file_name] = flashcards

# Check if decks.json exists and load the data
decks_json_path = '.internal/anki/decks.json'
decks = {}
if os.path.exists(decks_json_path):
    with open(decks_json_path, 'r') as f:
        decks = json.load(f)

# Define fields and template for the Anki flashcards
model_name = 'My Model'
field_names = ['Question', 'Answer']

# Generate a unique deck ID for each file
for file_name, flashcards in flashcards_by_file.items():
    base_deck_id = random.randint(10**9-1, 10**10-1)
    deck_id = base_deck_id
    data = {"action": "deckNamesAndIds", "version": 6}
    response = requests.post(url, headers=headers, json=data)
    existing_decks = response.json()["result"]
    while True:
        data = {"action": "deckNamesAndIds", "version": 6}
        if deck_id not in [d for d in existing_decks.values()]:
            break
        deck_id = base_deck_id + random.randint(1, 1000000)

    deck_name = os.path.splitext(file_name)[0]

    # Check if deck already exists in the dictionary
    if deck_name in decks:
        deck_id = decks[deck_name]
    else:
        # Create a new deck and add to the dictionary
        data = {
            "action": "createDeck",
            "version": 6,
            "params": {
                "deck": deck_name
            }
        }
        response = requests.post(url, headers=headers, json=data)
        deck_id = response.json()["result"]
        decks[deck_name] = deck_id

    # Create Anki model
    my_model_template = {
        'name': 'My Template',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    }

    my_model = genanki.Model(
        deck_id,
        model_name,
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[my_model_template],
    )

    # Create Anki deck for the file and add flashcards to it
    my_deck = genanki.Deck(deck_id, deck_name)
    for flashcard in flashcards:
        my_note = genanki.Note(
    model=my_model,
    fields=[str(flashcard[0]), str(flashcard[1])]
    )


    # Create Anki package and save to file
    my_package = genanki.Package(my_deck)
    my_package.write_to_file(f'out_anki/{deck_name}.apkg')

# Save the dictionary to the JSON file
with open(decks_json_path, 'w') as f:
    json.dump(decks, f)

print("Export successful!")

