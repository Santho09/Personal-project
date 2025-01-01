import os
import tempfile
from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS  # Import Flask-CORS
import PyPDF2
import docx

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the Hugging Face pipeline globally
summarizer = None

# Set a maximum number of tokens (e.g., 1024 for models like BART, T5, etc.)
MAX_TOKENS = 1024

# This function is used to load the model only once
def load_model():
    global summarizer
    summarizer = pipeline("summarization")

# Function to chunk the text if it's too long
def chunk_text(text, max_tokens=MAX_TOKENS):
    words = text.split()
    chunks = []
    chunk = []

    for word in words:
        if len(' '.join(chunk) + ' ' + word) <= max_tokens:
            chunk.append(word)
        else:
            chunks.append(' '.join(chunk))
            chunk = [word]

    if chunk:
        chunks.append(' '.join(chunk))

    return chunks

# Function to extract text from a PDF file
def extract_pdf_text(pdf_file_path):
    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        return text

# Function to extract text from a DOCX file
def extract_docx_text(docx_file_path):
    doc = docx.Document(docx_file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Function to extract text from a plain text file
def extract_txt_text(txt_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Define route for home
@app.route('/')
def home():
    return "Welcome to the Text Summarization API!"

# Define route for text summarization from uploaded file
@app.route('/summarize-file', methods=['POST'])
def summarize_file():
    if summarizer is None:
        return jsonify({"error": "Model is not loaded."}), 500
    
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({"error": "No file provided."}), 400
    
    file = request.files['file']
    
    # Debugging: Check if file is received
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400
    
    # Save the file to a temporary location
    try:
        # Create a temporary file to save the uploaded file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}")
        file.save(temp_file.name)  # Save the uploaded file to the temporary file
        temp_file.close()  # Close the temporary file so it can be processed
        
        # Debugging: Verify the temporary file is saved
        print(f"Temporary file saved at: {temp_file.name}")

        # Extract text from the uploaded file based on its extension
        text = ""
        if file.filename.endswith('.pdf'):
            text = extract_pdf_text(temp_file.name)
        elif file.filename.endswith('.docx'):
            text = extract_docx_text(temp_file.name)
        elif file.filename.endswith('.txt'):
            text = extract_txt_text(temp_file.name)
        else:
            return jsonify({"error": "Unsupported file type. Please upload a PDF, DOCX, or TXT file."}), 400

        if not text:
            return jsonify({"error": "Unable to extract text from the file."}), 400

        # If text is too long, break it into chunks
        chunks = chunk_text(text)
        summaries = []

        # Summarize each chunk and combine the summaries
        for chunk in chunks:
            summary = summarizer(chunk)
            summaries.append(summary[0]['summary_text'])

        # Combine the summaries of all chunks
        final_summary = ' '.join(summaries)

        # Clean up the temporary file
        os.remove(temp_file.name)

        return jsonify({"summary": final_summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define route for text summarization from manually entered text
@app.route('/summarize', methods=['POST'])
def summarize():
    if summarizer is None:
        return jsonify({"error": "Model is not loaded."}), 500
    
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided."}), 400
    
    text = data['text']
    
    if not text:
        return jsonify({"error": "Text cannot be empty."}), 400

    # If text is too long, break it into chunks
    chunks = chunk_text(text)
    summaries = []

    # Summarize each chunk and combine the summaries
    for chunk in chunks:
        summary = summarizer(chunk)
        summaries.append(summary[0]['summary_text'])

    # Combine the summaries of all chunks
    final_summary = ' '.join(summaries)

    return jsonify({"summary": final_summary})

# Run the app, ensure to use `if __name__ == "__main__":` in Windows
if __name__ == "__main__":
    load_model()  # Load the model before running the app
    app.run(debug=True, use_reloader=False)  # use_reloader=False to avoid multiple model loading
