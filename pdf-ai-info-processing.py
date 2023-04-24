from PyPDF2 import PdfReader
import openai
import json
import sys
import os
def openai_query(prompt):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        max_tokens=1500,
        temperature=0.3
    )
    return response['choices'][0]['text']

def query(prompt_suffix):
    prompt_prefix = """Can you give me an answer with the structure of JSON with the core ideas of this text in answer/question form? Only the JSON with the fields Question and Answer, do not add any other information as explanation or conclusion. Also, put it in plain text and make sure the correct position of { } simbols. Only use ASCII characters. Do not add a confirmation as 'sure' neither say 'in this example'. Follow this example:

    '[
        {
            "Question": "¿Cómo se realiza el envío de paquetes IP entre dispositivos de redes diferentes?",
            "Answer": "El envío se realiza mediante un router. Si el destino está en la misma red, se resuelve la MAC del destino y se envía el paquete. Si el destino está en otra red, se resuelve la MAC de la puerta de enlace y se le envía la trama."
        },
        {
            "Question": "2¿Cómo se realiza el envío de paquetes IP entre dispositivos de redes diferentes?",
            "Answer": "El2 envío se realiza mediante un router. Si el destino está en la misma red, se resuelve la MAC del destino y se envía el paquete. Si el destino está en otra red, se resuelve la MAC de la puerta de enlace y se le envía la trama."
        }
    ]'
    """

    # Generate response from OpenAI API
    response_text = openai_query(prompt_prefix + prompt_suffix)
    print(response_text)
    # Construct prompt for correcting JSON syntax
    prompt_correction = """Please correct the JSON output below to ensure it meets the following requirements:
- The JSON structure should match the example "[
    {
        "Question": "exa",
        "Answer": "exe"
    },
    {
        "Question": "exi",
        "Answer": "exu"
    }
]".
- The 'Question' and 'Answer' fields should be present for each item.
- The JSON should be properly formatted with correct braces, brackets, commas, and quotation marks.
- This is the last requirement, make sure all information in " " after this is inside the JSON structure.
"
    """

    # Generate response to correct JSON syntax
    prompt = prompt_correction + response_text + """ " """
    print(prompt)
    corrected_response_text = openai_query(prompt)

    # Return corrected response
    return corrected_response_text

def generate_response_text(num_pages):
    response_text = ""
    response_text_end = ""
    prompt_suffix=""

    for i in range(num_pages):
        page = reader.pages[i]
        text = page.extract_text()
        print("here")

        if len(prompt_suffix + text)+1128 < 4096:
            prompt_suffix += f"\n{text}"
        else:
            print(f"{i}/{num_pages}")
            response_text_end+=query(prompt_suffix)
            prompt_suffix = f"\n{text}"

    response_text_end+=query(prompt_suffix)

    return response_text_end

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
    
    # Initialize the prompt string with the CSV format instructions
    final_answer=generate_response_text(6)

    # # Loop through each page in the PDF and extract the text
    # for i in range(num_pages):
    #     page = reader.pages[i]
    #     text = page.extract_text()
    # 
    #     # Add the current page text to the prompt if the resulting prompt has less than 4096 tokens
    #     if len(prompt_prefix1 + prompt_suffix1 + text) < 4096:
    #         prompt_suffix1 += f"\n{text}"
    #     else:
    #         # Query OpenAI API with the current prompt
    #         prompt = prompt_prefix1 + prompt_suffix1
    #         # print(prompt)
    #         print(f"{i}/{num_pages}")
    #         response = openai.Completion.create(
    #             model="text-davinci-002",
    #             prompt=prompt,
    #             max_tokens=1500,
    #             temperature=0.3
    #         )
    #         temp_response=response['choices'][0]['text']
    #         prompt=prompt_correction+temp_response
    #         response = openai.Completion.create(
    #             model="text-davinci-002",
    #             prompt=prompt,
    #             max_tokens=1500,
    #             temperature=0.3
    #         )
    #         response_text += response['choices'][0]['text']
    #
    # 
    #         # Reset the prompt suffix to the remaining text that didn't fit in the previous prompt
    #         prompt_suffix = f"\n{text}"
    #     
    # # Query OpenAI API with the final prompt
    # prompt = prompt_prefix + prompt_suffix
    # response = openai.Completion.create(
    #     model="text-davinci-002",
    #     prompt=prompt,
    #     max_tokens=1500,
    #     temperature=0.3
    # )
    # response_text += response['choices'][0]['text']

    print(final_answer)
    custom_filename = os.path.splitext(filename)[0]
    json_path = os.path.join('out_json', custom_filename)
    json_name = f"{json_path}.json"
    print(json_name)
    
    with open(json_name, 'w') as file:
        file.write(final_answer)    # subprocess.call("./clean_csv.sh")
    
