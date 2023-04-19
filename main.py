from PyPDF2 import PdfReader
import openai
import time
import csv
import json
import subprocess

with open("key.json") as f:
    data = json.load(f)

openai.api_key = data["openai_api_key"]

pdf_path = "example.pdf"

# Create a PdfReader object from the PDF file
reader = PdfReader(pdf_path)

# Get the number of pages in the PDF
num_pages = len(reader.pages)

# Initialize the prompt string with the CSV format instructions
prompt_prefix = "Can you give me an answer with the structure of csv with the core ideas of this text in answer/question form? Only the CSV, do not add any other information as explanation or conclusion. Also, put it in plain text. Do not add a confirmation as 'sure' neither say 'in this example'. Also, at the beginning, do not add 'Question,Answer'."
prompt_suffix = ""
response_text=""
# Loop through each page in the PDF and extract the text
for i in range(num_pages):
    page = reader.pages[i]
    text = page.extract_text()

    # Add the current page text to the prompt if the resulting prompt has less than 4096 tokens
    if len(prompt_prefix + prompt_suffix + text) < 4096:
        prompt_suffix += f"\n{text}"
    else:
        # Query OpenAI API with the current prompt
        prompt = prompt_prefix + prompt_suffix
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            max_tokens=1500,
            temperature=0.3
        )
        response_text += response['choices'][0]['text']
        print(response_text)

        # Reset the prompt suffix to the remaining text that didn't fit in the previous prompt
        prompt_suffix = f"\n{text}"
    
# Query OpenAI API with the final prompt
prompt = prompt_prefix + prompt_suffix
response = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    max_tokens=1500,
    temperature=0.3
)
response_text += response['choices'][0]['text']

print(response_text)
with open('response.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow([response_text])


subprocess.call("./clean_csv.sh")
