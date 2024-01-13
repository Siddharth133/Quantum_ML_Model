# import streamlit as st
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# import os
# import re
# import fitz
# st.set_option('server.staticDir', 'static')
# model_name = "gpt2"
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# model = GPT2LMHeadModel.from_pretrained(model_name)
#
# # Function to extract text from PDF
# def extract_text_from_pdf(file_path):
#     if not os.path.exists(file_path):
#         return "File not found.", False
#     doc = fitz.open(file_path)
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     return text, True
#
# def generate_answer(question, context):
#     input_text = f"Context: {context[:1024]}\nQuestion: {question}\nAnswer:"
#     input_ids = tokenizer.encode(input_text, return_tensors='pt')
#
#     # Generate a response with a maximum length
#     output = model.generate(input_ids, max_length=300, num_return_sequences=1, no_repeat_ngram_size=2, pad_token_id=tokenizer.eos_token_id)
#     generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
#
#     # Use regex to extract only the complete answer part
#     match = re.search(r"Answer: ([\s\S]*?\.)", generated_text)
#     if match:
#         return match.group(1).strip()
#     else:
#         return "No answer found."
#
# # Streamlit app
# def main():
#     st.title("ChatPDF - Ask Questions from PDF")
#
#     file_path = "DATASET_ON_MARINE_ANIMALS.txt"
#     question = st.text_input("Enter your question")
#
#     if st.button("Answer"):
#         if file_path and question:
#             # Extract text from the PDF
#             text, file_exists = extract_text_from_pdf(file_path)
#
#             if not file_exists:
#                 st.write("Error: File not found.")
#             else:
#                 # Generate an answer
#                 answer = generate_answer(question, text)
#                 st.write("Answer:", answer)
#         else:
#             st.write("Please enter a valid file path and a question.")
#
#
# # Streamlit app
# def main():
#     st.title("ChatPDF - Ask Questions from PDF")
#
#     file_path = "DATASET_ON_MARINE_ANIMALS.txt"
#     question = st.text_input("Enter your question")
#
#     if st.button("Answer"):
#         if file_path and question:
#             # Extract text from the PDF
#             text, file_exists = extract_text_from_pdf(file_path)
#
#             if not file_exists:
#                 st.write("Error: File not found.")
#             else:
#                 # Generate an answer
#                 answer = generate_answer(question, text)
#                 st.write("Answer:", answer)
#         else:
#             st.write("Please enter a valid file path and a question.")
#
# if __name__ == '__main__':
#     main()



import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os
import re
import PyPDF2


model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Function to extract text from PDF using PyPDF2
def extract_text_from_pdf(file_path):
    if not os.path.exists(file_path):
        return "File not found.", False
    text = ""
    try:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extractText()
    except Exception as e:
        return str(e), False
    return text, True

def generate_answer(question, context):
    input_text = f"Context: {context[:1024]}\nQuestion: {question}\nAnswer:"
    input_ids = tokenizer.encode(input_text, return_tensors='pt')

    # Generate a response with a maximum length
    output = model.generate(input_ids, max_length=300, num_return_sequences=1, no_repeat_ngram_size=2, pad_token_id=tokenizer.eos_token_id)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # Use regex to extract only the complete answer part
    match = re.search(r"Answer: ([\s\S]*?\.)", generated_text)
    if match:
        return match.group(1).strip()
    else:
        return "No answer found."

# Streamlit app
def main():
    st.title("ChatPDF - Ask Questions from PDF")

    file_path = "DATASET_ON_MARINE_ANIMALS.txt"
    question = st.text_input("Enter your question")

    if st.button("Answer"):
        if file_path and question:
            # Extract text from the PDF using PyPDF2
            text, file_exists = extract_text_from_pdf(file_path)

            if not file_exists:
                st.write("Error: File not found.")
            else:
                # Generate an answer
                answer = generate_answer(question, text)
                st.write("Answer:", answer)
        else:
            st.write("Please enter a valid file path and a question.")

if __name__ == '__main__':
    main()
