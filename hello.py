from flask import Flask, request
from flask import send_file

import PyPDF2
import os

app = Flask(__name__)

def extract_pdf_pages(words):
    # Hardcoded file path for the PDF file
    pdf_file_path = '/home/sibi/Downloads/Test/1.pdf'

    # Open the PDF file in read-binary mode
    with open(pdf_file_path, 'rb') as file:
        # Create a PDF reader object
        reader = PyPDF2.PdfReader(file)

        # Iterate over each word in the list
        for word in words:
            # Create a PDF writer object
            writer = PyPDF2.PdfWriter()

            # Iterate over each page in the PDF
            for page in range(len(reader.pages)):
                # Get the text of the page
                text = reader.pages[page].extract_text().lower() # Convert the text to lower case
                # Check if the word is in the text, ignoring case
                if word.lower() in text:
                    # If the word is found, add the page to the PDF writer object
                    writer.add_page(reader.pages[page])

            # Save the extracted pages to a new PDF file in the same folder as the input pdf
            output_file_path = os.path.join(os.path.dirname(pdf_file_path), f'{word}.pdf')
            with open(output_file_path, 'wb') as output:
                writer.write(output)
    return output_file_path

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        words = request.form["words"].strip().split(",")
        file_path = extract_pdf_pages(words)
        return send_file(file_path, as_attachment=True)

    return '''
        <form method="post">
            <input type="text" name="words">
            <input type="submit" value="Submit">
        </form>
    '''

if __name__ == "__main__":
    app.run()
