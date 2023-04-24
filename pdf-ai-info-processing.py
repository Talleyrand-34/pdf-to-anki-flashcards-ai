from PyPDF2 import PdfReader
import openai
import csv
import sys
import os
import re
import json
import subprocess

def openai_query(prompt):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        max_tokens=1500,
        temperature=0.3
    )
    return response['choices'][0]['text']

def query(prompt_suffix):
    prompt_prefix = "Can you give me an answer with the structure of csv with the core ideas of this text in answer/question form? Only the CSV, do not add any other information as explanation or conclusion. Also, put it in plain text. Do not add a confirmation as 'sure' neither say 'in this example'. Also, at the beginning, do not add 'Question,Answer'. Also when you want to add a comma to the question or the answer which is part of the string substitute it by '|'"

    response_text = openai_query(prompt_prefix + prompt_suffix)
    print(response_text)
    return response_text

def replace_commas_after_question(s):
    result = []
    split_by_question = s.split("?")

    for i, segment in enumerate(split_by_question):
        if i > 0:
            first_comma_idx = segment.find(",")
            if first_comma_idx != -1:
                segment = (
                    segment[: first_comma_idx + 1]
                    + segment[first_comma_idx + 1 :].replace(",", "|")
                )
        result.append(segment)

    return "?".join(result)



def generate_response_text(num_pages):
    response_text_end = ""
    prompt_suffix=""

    for i in range(num_pages):
        page = reader.pages[i]
        text = page.extract_text()
        print("here")

        if len(prompt_suffix + text)+448 < 4096:
            prompt_suffix += f"\n{text}"
        else:
            print(f"{i}/{num_pages}")
            response_text_end+=query(prompt_suffix)
            prompt_suffix = f"\n{text}"

    response_text_end=replace_commas_after_question(response_text_end)
    return response_text_end

with open("key.json") as f:
    data = json.load(f)

pdf_files_path = './pdf_files'
openai.api_key = data["openai_api_key"]
if '-a' in sys.argv:
    pdf_files = [f for f in os.listdir(pdf_files_path) if f.endswith('.pdf')]
elif '-f' in sys.argv:
    # Get filenames from command line argument
    filenames = sys.argv[sys.argv.index('-f')+1:]
    pdf_files = [f for f in filenames if f.endswith('.pdf')]
else:
    print("Error: Please specify either -a to process all PDF files in the directory, or -f followed by a list of filenames to process.")
    exit(1)
for filename in os.listdir(pdf_files_path):
    pdf_path = os.path.join(pdf_files_path, filename)
    reader = PdfReader(pdf_path)
    
    num_pages = len(reader.pages)
    final_answer = generate_response_text(num_pages)
    
    lines = final_answer.split('\n')
    failed_lines = []
    
    for line in lines:
        if not re.match('.*,.*', line):
            failed_lines.append(line)

    final_answer = '\n'.join([line for line in lines if re.match('.*,.*', line)])
    failed_lines = '\n'.join(failed_lines)
    print(final_answer)
    print("//////////")
    print(failed_lines)
    print("//////////")
    custom_filename = os.path.splitext(filename)[0]
    csv_path = os.path.join('out_csv', custom_filename)
    csv_name = f"{csv_path}.csv"
    fail_path = os.path.join('failed', custom_filename)
    fail_name = f"{fail_path}.csv"
    print(csv_name)
    
    with open(csv_name, 'w') as file:
        file.write(final_answer)   
        
    with open(fail_name + ".failed", 'w') as file:
        file.write(failed_lines)   
    subprocess.call("./clean_csv.sh")   
