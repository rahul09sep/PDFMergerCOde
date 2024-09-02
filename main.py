from flask import Flask, request, render_template, send_file
import os
import shutil
import fitz  # PyMuPDF

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
MERGED_FOLDER = os.path.join(os.getcwd(), 'merged')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MERGED_FOLDER'] = MERGED_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    # Clear previous uploads and merged files
    shutil.rmtree(app.config['UPLOAD_FOLDER'], ignore_errors=True)
    shutil.rmtree(app.config['MERGED_FOLDER'], ignore_errors=True)
    os.makedirs(app.config['UPLOAD_FOLDER'])
    os.makedirs(app.config['MERGED_FOLDER'])

    for key, uploaded_file in request.files.items():
        if uploaded_file.filename != '':
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(pdf_path)

    merged_pdf_path = os.path.join(app.config['MERGED_FOLDER'], 'merged-pdf.pdf')
    merge_pdfs(app.config['UPLOAD_FOLDER'], merged_pdf_path)
    print("Merged PDF Path:", merged_pdf_path)
    return send_file(merged_pdf_path, as_attachment=True)

def merge_pdfs(input_folder, output_path):
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]

    pdf_writer = fitz.open()

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_reader = fitz.open(pdf_path)
        pdf_writer.insert_pdf(pdf_reader, from_page=0, to_page=pdf_reader.page_count - 1)

    pdf_writer.save(output_path)
    pdf_writer.close()

if __name__ == '__main__':
    app.run(debug=True)