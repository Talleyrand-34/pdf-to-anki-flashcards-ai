from PyPDF2 import PdfReader
import openai
import csv
import json
import subprocess
import sys
import os
with open("key.json") as f:
    data = json.load(f)

pdf_files_path = './pdf_files'
openai.api_key = data["openai_api_key"]
if '-a' in sys.argv:
    pdf_files = [f for f in os.listdir(pdf_files_path) if f.endswith('.pdf')]


for filename in os.listdir(pdf_files_path):
    pdf_path = os.path.join(pdf_files_path, filename)
    # Create a PdfReader object from the PDF file
    reader = PdfReader(pdf_path)
    
    # Get the number of pages in the PDF
    # num_pages = len(reader.pages)
    num_pages = 7
    
    # Initialize the prompt string with the CSV format instructions
    prompt_prefix ="Can you give me an answer with the structure of csv with the core ideas of this text in answer/question form? Only the JSON with the fields Question and Answer, do not add any other information as explanation or conclusion. Also, put it in plain text and make sure the correct position of { } simbols. Do not add a confirmation as 'sure' neither say 'in this example'."  
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
            print(prompt)
            print(f"{i}/{num_pages}")
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=prompt,
                max_tokens=1500,
                temperature=0.3
            )
            response_text += response['choices'][0]['text']
    
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

    # print(response_text)
    custom_filename = os.path.splitext(filename)[0]
    json_path = os.path.join('out_json', custom_filename)
    json_name = f"{json_path}.json"
    print(json_name)
    
    with open(json_name, 'w') as file:
        json.dump({'Question': response_text}, file)
    # subprocess.call("./clean_csv.sh")
    
