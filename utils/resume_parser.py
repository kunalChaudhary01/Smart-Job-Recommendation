import os
import PyPDF2
from docx import Document


def extract_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    text = ""

    if extension == ".pdf":

        with open(file_path, "rb") as file:

            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                text += page.extract_text() or ""

    elif extension == ".docx":

        document = Document(file_path)

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

    return text