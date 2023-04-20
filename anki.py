import csv
import genanki# Read flashcards from CSV
flashcards = []
with open('response.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        flashcards.append(row)
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

# Create Anki deck
my_deck = genanki.Deck(1607392319, 'My Deck')

# Add flashcards to the Anki deck
for flashcard in flashcards:
    my_note = genanki.Note(
        model=my_model,
        fields=[flashcard[0], flashcard[1]]
    )
    my_deck.add_note(my_note)

# Create Anki package and save to file
my_package = genanki.Package(my_deck)
my_package.write_to_file('my_deck.apkg')

