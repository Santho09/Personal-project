# Summarizer app
Here’s a `README.md` file for your project that you can upload to GitHub. It provides a clear overview of the project, its features, installation steps, usage, and other relevant details.

---

# Text Summarization API

This project is a Flask-based web application that performs text summarization using Hugging Face's `transformers` library. It supports summarizing both plain text entered manually and text extracted from uploaded files (PDF, DOCX, and TXT).

## Features

- **Text Summarization**: Summarizes long text by breaking it into chunks and applying a pre-trained summarization model.
- **File Support**: Supports PDF, DOCX, and TXT files for summarization.
- **Manual Text Input**: Summarizes text directly entered into the API.
- **CORS Support**: Cross-Origin Resource Sharing (CORS) is enabled, allowing the API to be accessed by other applications.

## Technologies Used

- Python
- Flask
- Hugging Face's `transformers` library
- PyPDF2 for PDF text extraction
- python-docx for DOCX text extraction
- Flask-CORS for enabling cross-origin requests

## Setup and Installation

Follow the steps below to set up the project locally.

### Prerequisites

- Python 3.x
- `pip` (Python package manager)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/text-summarization-api.git
   cd text-summarization-api
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Windows:
   
     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:
   
     ```bash
     source venv/bin/activate
     ```

4. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` should include:

   ```
   flask
   flask-cors
   transformers
   PyPDF2
   python-docx
   ```

5. **Run the Flask application:**

   ```bash
   python app.py
   ```

   The app should now be running at `http://127.0.0.1:5000/`.

## API Endpoints

### 1. `/`
   - **Description**: Home route.
   - **Method**: `GET`
   - **Response**: Returns a welcome message.

### 2. `/summarize`
   - **Description**: Summarizes manually entered text.
   - **Method**: `POST`
   - **Request Body**: JSON with a `text` field containing the text to summarize.
   - **Response**: JSON containing the summarized text.
   
   #### Example Request:
   ```bash
   curl -X POST http://127.0.0.1:5000/summarize \
   -H "Content-Type: application/json" \
   -d '{"text": "Your long text here."}'
   ```

   #### Example Response:
   ```json
   {
     "summary": "Summarized text."
   }
   ```

### 3. `/summarize-file`
   - **Description**: Summarizes text extracted from an uploaded file.
   - **Method**: `POST`
   - **Request Body**: A `multipart/form-data` request with the file (`pdf`, `docx`, or `txt`).
   - **Response**: JSON containing the summarized text.

   #### Example Request:
   ```bash
   curl -X POST http://127.0.0.1:5000/summarize-file \
   -F "file=@path_to_your_file.pdf"
   ```

   #### Example Response:
   ```json
   {
     "summary": "Summarized text from the file."
   }
   ```

## Usage Instructions

1. **Manual Text Input**: Use the `/summarize` route to send long text as JSON and receive a summarized version.
2. **File Upload**: Upload a `.pdf`, `.docx`, or `.txt` file using the `/summarize-file` route, and the app will return a summarized version of the text.

## Handling Errors

The API handles the following error cases:

- If no file is provided in the request, the response will include an error message.
- If the uploaded file type is unsupported, the API will respond with an error.
- If the text is too long, the text will be split into chunks, and each chunk will be summarized.

## Development and Debugging

- To debug issues with file uploads, the app saves the uploaded file temporarily and prints the file path. Check the console output for debugging information.
- The `use_reloader=False` option in `app.run()` ensures the summarization model is not loaded multiple times.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

This `README.md` file includes instructions for setting up, using, and testing the API. You can customize this further with your GitHub username and any specific details related to your project.

Let me know if you'd like to add any specific sections!
