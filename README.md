# 🧠 Anton AI Assistant

A modern, feature-rich AI assistant desktop application built with **Python** and **PySide6**, featuring **voice interaction**, **file management**, and **web search** capabilities.

![Anton AI Assistant](https://img.shields.io/badge/Anton-AI%2520Assistant-purple?style=for-the-badge)

---

## 🚀 Features

- 🤖 **AI-Powered Conversations:** Powered by **Google Gemini** for intelligent responses  
- 🎙️ **Voice Interaction:** Speak to Anton and get voice responses  
- 📁 **File Management:** Create, read, update, and manage files directly through chat  
- 🌐 **Web Search:** Real-time information retrieval when needed  
- 🎨 **Modern UI:** Beautiful dark theme inspired by **Perplexity**  
- 💬 **Chat Interface:** Smooth, animated chat bubbles with timestamps  
- 🔍 **File Browser:** Built-in file explorer for your project files  

---

## 📋 Prerequisites

- **Python 3.8** or higher  
- **Google Gemini API key**  
- **Google Custom Search API key** *(optional, for web search)*

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd anton-ai-assistant
```

## 🛠️ Installation

### 2. Install Required Dependencies

```bash
pip install -r requirements.txt

3. Set Up Environment Variables
```
Create a .env file in the project root directory and add your API keys:

GEMINI_API_KEY=your_gemini_api_key_here
CUSTOM_SEARCH_KEY=your_custom_search_key_here
SEARCH_ENGINE_ID=your_search_engine_id_here

🔑 Getting API Keys
Google Gemini API Key

Go to Google AI Studio

Sign in with your Google account

Create a new API key

Copy the key and add it to your .env file as GEMINI_API_KEY

Google Custom Search API (Optional - for Web Search)

Visit Google Cloud Console

Create a new project or select an existing one

Enable the Custom Search JSON API

Create credentials (API key)

Set up a Custom Search Engine at Programmable Search Engine

Add the Search Engine ID and API key to your .env file

🎯 Usage
Run the Application
python anton_app.py

Basic Interactions

Type your questions in the input field

Click the microphone button for voice input

Use the file browser to manage your files

Send commands like:

create file [filename] with [content description]
read file [filename]
update file [filename] with [new content]
append to file [filename] with [additional content]
delete file [filename]
open file [filename]
list files

🗂️ Project Structure
anton-ai-assistant/
├── anton_app.py          # Main application file
├── .env                  # Environment variables (create this)
├── requirements.txt      # Python dependencies
├── Anton_Files/          # Directory for managed files
└── README.md             # This file

📁 File Management

Anton automatically creates and manages an Anton_Files directory where all your files are stored.
You can:

📝 Create new files with AI-generated content

📖 Read and get summaries of file contents

🔄 Update files with new AI-generated content

➕ Append additional content to existing files

🗑️ Delete files you no longer need

📂 Open files in their default applications

🎙️ Voice Commands

Click the microphone button to activate voice input. The application will:

Show a visual indicator when listening

Convert your speech to text

Process your query and provide a response

Read responses aloud using text-to-speech

🔧 Configuration
Using Different AI Models

Modify the model in the code by changing this line in anton_app.py:

model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')


Available Gemini Models:

gemini-2.0-flash-thinking-exp (current)

gemini-1.5-flash

gemini-1.5-pro

gemini-1.0-pro

Customizing the Theme

Modify the color scheme in the ThemeColors class:

class ThemeColors:
    PRIMARY = "#0F0F17"           # Main background
    ACCENT = "#6F58C4"            # Primary accent color
    TEXT_PRIMARY = "#FFFFFF"      # Main text color
    # ... other colors

🐛 Troubleshooting
Common Issues
🔐 API Key Errors

Ensure your Gemini API key is valid and in the .env file

Check that it has the necessary permissions

🎤 Voice Recognition Not Working

Ensure a microphone is connected

Check system microphone permissions

Verify internet connection for Google Speech Recognition

📁 File Operations Failing

Ensure the Anton_Files directory has write permissions

Avoid using invalid characters in filenames

⚙️ Module Import Errors

Run pip install -r requirements.txt

Use Python 3.8+

📦 Dependencies

Key packages used:

PySide6 – Modern GUI framework

google-generativeai – Gemini AI integration

pyttsx3 – Text-to-speech functionality

speechrecognition – Speech-to-text capabilities

python-dotenv – Environment variable management

🔒 Privacy & Security

API keys are stored locally in .env

File operations occur only in the Anton_Files directory

Voice data is processed by Google’s Speech Recognition

No external data storage beyond API requirements

📄 License

This project is for educational and personal use.
Please comply with Google’s API Terms of Service.

🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

📞 Support

If you encounter issues:

Check the Troubleshooting section above

Ensure all API keys are properly configured

Verify all dependencies are installed correctly

⚠️ Note: This application requires an active internet connection for AI responses and voice recognition features.
