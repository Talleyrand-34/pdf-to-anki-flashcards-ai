from PyPDF2 import PdfReader
import openai
import time



openai.api_key = "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"
pdf_path = "example.pdf"

# Create a PdfReader object from the PDF file
reader = PdfReader(pdf_path)

# Get the number of pages in the PDF
num_pages = len(reader.pages)

# Initialize the prompt string with the CSV format instructions
prompt = "Can you give me an answer with the structure of csv with the core ideas of this text in answer/question form? Only the CSV, do not add any other information as explanation or conclusion. Also, put it in plain text. Do not add a confirmation as 'sure' neither say 'in this example'. Also, at the beginning, do not add 'Question,Answer'."

# Loop through each page in the PDF and extract the text
for i in range(num_pages):
    page = reader.pages[i]
    text = page.extract_text()
    prompt += f"\n{text}"

print(prompt)

response = openai.Completion.create(
            #engine="text-davinci-003",
            model= "text-davinci-003",
            prompt=prompt,
            max_tokens=1500,
            temperature=0.3
        )
response_text = response['choices'][0]['text']
print(response_text)





