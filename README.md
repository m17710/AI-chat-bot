# AI Q&A Chatbot

A simple Streamlit chatbot that sends questions to the Groq API and displays AI-generated answers.

## Setup

1. Create a Python virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   - Windows PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows Command Prompt:
     ```cmd
     .\venv\Scripts\activate.bat
     ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your Groq API key:

   ```env
   GROQ_API_KEY="your_api_key_here"
   ```

5. Run the app:

   ```bash
   streamlit run app.py
   ```

## Usage

- Type a question into the text box.
- Click `Ask`.
- The AI answer will appear below.
- Click `Clear conversation` to reset chat history.

## Notes

- Do not commit your `.env` file to source control.
- If you see errors, verify your API key and internet connection.
