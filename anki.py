import os
import csv
import genanki

# Read flashcards from CSV files
flashcards_by_file = {}
for file_name in os.listdir('out_csv'):
    if file_name.endswith('.csv') and not file_name.endswith('.bck.csv'):
        with open(f'out_csv/{file_name}', newline='') as csvfile:
            reader = csv.reader(csvfile)
            flashcards = [row for row in reader]
        flashcards_by_file[file_name] = flashcards

# Define fields and template for the Anki flashcards
model_name = 'My Model'
field_names = ['Question', 'Answer']

my_model_template = {
    'name': 'My Template',
    'qfmt': '{{Question}}',
    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
}

# Create Anki model
my_model = genanki.Model(
    1607392319,
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
    my_package.write_to_file(f'{deck_name}.apkg')
