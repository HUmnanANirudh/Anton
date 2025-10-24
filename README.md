# Anton AI Assistant

A **modern desktop AI assistant** built with **Python** and **PySide6**, featuring **Google Gemini integration**, **voice commands**, **file management**, and **web search**

![Anton AI Assistant](https://img.shields.io/badge/Anton-AI_Assistant-purple?style=for-the-badge)

---

## Features

- AI-powered chat using **Google Gemini**  
- Voice input & speech output  
- File management (create, read, update, delete)  
- Web search with Google Custom Search  

---

## Installation

### Clone and Install
```bash
git clone <your-repo-url>
cd anton-ai-assistant
pip install -r requirements.txt
```

## Add API Keys

Create a `.env` file in the root directory:

GEMINI_API_KEY=your_gemini_api_key_here
CUSTOM_SEARCH_KEY=your_custom_search_key_here
SEARCH_ENGINE_ID=your_search_engine_id_here

yaml
Copy code

---

## Usage

Run the app:

python anton_app.py

markdown
Copy code

Then you can:

- Type or speak to Anton  
- Manage files easily  
- Search the web  
- Hear voice replies  

### Example Commands

create file notes.txt with AI summary
read file notes.txt
list files

yaml
Copy code

---

## Tech Stack

- PySide6 – Modern GUI  
- Google Gemini API – AI model  
- SpeechRecognition – Voice input  
- pyttsx3 – Voice output  
- python-dotenv – Environment setup  

---

## Configuration

Change the Gemini model in `anton_app.py`:

```python
model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp")
```
## License
For educational and personal use only.
Comply with Google’s API Terms of Service.
