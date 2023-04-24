import os
import csv
import random
import genanki
import requests

def upload_deck_to_anki(deck_path):
    with open(deck_path, 'rb') as f:
        deck_data = f.read()

    print(deck_path)

    # Get the path of the script file
    script_path = os.path.abspath(__file__)
    
    # Get the directory containing the script file
    script_dir = os.path.dirname(script_path)
    
    # The variable 'file' should be defined before this line
    
    # Build the new path by combining the script directory, "out_anki", and the variable 'file'
    new_path = os.path.join(script_dir,  deck_path)

    print("New path:", new_path)

    payload = {
        "action": "importPackage",
        "version": 6,
        "params": {
            "path": f"{new_path}"
        }
    }

    response = requests.post('http://localhost:8765', json=payload)
    response.raise_for_status()
    print(response.json())
    return response.json()

# Read flashcards from CSV files
flashcards_by_file = {}
for file_name in os.listdir('out_csv'):
    if file_name.endswith('.csv'):
        flashcards = []
        with open(f'out_csv/{file_name}', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 2:
                    flashcards.append((row[0], row[1]))
        flashcards_by_file[file_name] = flashcards


# Define fields and template for the Anki flashcards
model_name = 'My Model'
field_names = ['Question', 'Answer']
nuumber_deck=random.randint(10**9-1,10**10 -1)

my_model_template = {
    'name': 'My Template',
    'qfmt': '{{Question}}',
    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
}

# Create Anki model
my_model = genanki.Model(
    nuumber_deck,
    model_name,
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[my_model_template],
)

# Create Anki deck for each file and add flashcards to it

for file_name, flashcards in flashcards_by_file.items():
    deck_name = os.path.splitext(file_name)[0]
    my_deck = genanki.Deck(1607392319, deck_name)
    for flashcard in flashcards:
        my_note = genanki.Note(
            model=my_model,
            fields=[flashcard[0], flashcard[1]]
        )
        my_deck.add_note(my_note)
    # Create Anki package and save to file
    my_package = genanki.Package(my_deck)
    output_file_path = f'out_anki/{deck_name}.apkg'
    my_package.write_to_file(output_file_path)

    # Upload the deck to Anki using AnkiConnect API
    try:
        upload_deck_to_anki(output_file_path)
        print(f'Successfully uploaded {deck_name} to Anki.')
    except Exception as e:
        print(f'Error uploading {deck_name} to Anki: {e}')

