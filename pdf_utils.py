import os
import PyPDF2


def pdf_to_text(pdf_file_name, txt_file_name):
    # Open the PDF file in read-binary mode
    with open(pdf_file_name, "rb") as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ""

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    # Write the extracted text to a text file
    with open(txt_file_name, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)


def pdf_to_text_all():
    pdf_directory = "product_inserts/pdf/"
    txt_directory = "product_inserts/txt/"
    for pdf_file_name in os.listdir(pdf_directory):
        print(pdf_directory + pdf_file_name)
        txt_file_name = os.path.splitext(pdf_file_name)[0] + ".txt"
        print(txt_directory + txt_file_name)
        pdf_to_text(pdf_directory + pdf_file_name, txt_directory + txt_file_name)

pdf_to_text_all()