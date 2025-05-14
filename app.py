# import os
# import subprocess
# import sys
# from dotenv import load_dotenv
# from flask import Flask, render_template, request, jsonify, send_from_directory
# import threading
# import time
# import json

# # Load environment variables
# load_dotenv()
# AiKey = os.getenv("GEMINI_API_KEY")
# SearchId = os.getenv("SEARCH_ENGINE_ID")
# SearchKey = os.getenv("CUSTOM_SEARCH_KEY")

# import google.generativeai as genai
# from googleapiclient.discovery import build

# # Configure Gemini API
# genai.configure(api_key=AiKey)
# model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')

# # Initialize chat
# chat = model.start_chat(history=[])

# # Anton Search function
# def Anton_Search(query, num_results=7):
#     service = build("customsearch", "v1", developerKey=SearchKey)
#     results = service.cse().list(q=query, cx=SearchId, num=num_results).execute()

#     search_results = []
#     if "items" in results:
#         for item in results["items"]:
#             search_results.append({
#                 "title": item["title"],
#                 "link": item["link"],
#                 "snippet": item.get("snippet", "")
#             })
#     return search_results

# # Should Anton search function
# def Should_Anton_search(user_query):
#     model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')
#     decision_prompt = f"""The user asked: "{user_query}" .
#     Determine if you need to search the web for up-to-date information.  
#     Respond ONLY with 'yes' or 'no'. If the question involves recent news, real-time events, or changing data, say 'yes'.  
#     Otherwise, say 'no'."""
#     response = model.generate_content(decision_prompt).text.strip().lower()
#     return "yes" in response

# # Anton's Response function
# def Antons_Response(user_query):
#     model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')

#     if user_query.lower() in ["who are you", "who are you ?", "what are you", "what are you ?", "introduce yourself"]:
#         return "I am Anton, How can Anton help you today?"

#     if Should_Anton_search(user_query):
#         search_results = Anton_Search(user_query)
#         search_info = "\n".join([
#             f"Title: {res['title']}\nURL: {res['link']}\nSnippet: {res['snippet']}\n"
#             for res in search_results
#         ])
#         final_prompt = f"""The user asked:"{user_query}" 
#         Here are relevant Anton's web search results:  
#         {search_info}  
#         Based on this, generate the best possible answer."""

#         final_response = model.generate_content(final_prompt).text
#     else:
#         final_response = model.generate_content(user_query).text

#     return final_response

# # File management setup
# FILES_DIR = "Anton_Files"
# os.makedirs(FILES_DIR, exist_ok=True)

# def get_file_path(filename: str) -> str:
#     """Returns the full path of the file inside Anton_Files directory."""
#     return os.path.join(FILES_DIR, filename)

# def create_file(filename: str, content: str) -> str:
#     """Creates a new file with the provided content in Anton_Files directory."""
#     filepath = get_file_path(filename)
#     try:
#         with open(filepath, 'w', encoding='utf-8') as f:
#             f.write(content)
#         return f"File '{filename}' created at '{filepath}'."
#     except Exception as e:
#         return f"Error creating file: {e}"

# def read_file(filename: str) -> str:
#     """Reads and returns the content of a file."""
#     filepath = get_file_path(filename)
#     if not os.path.exists(filepath):
#         return f"File '{filename}' does not exist."
#     try:
#         with open(filepath, 'r', encoding='utf-8') as f:
#             content = f.read()
#         return content
#     except Exception as e:
#         return f"Error reading file: {e}"

# def update_file(filename: str, new_content: str) -> str:
#     """Overwrites the file with new content."""
#     filepath = get_file_path(filename)
#     if not os.path.exists(filepath):
#         return f"File '{filename}' does not exist."
#     try:
#         with open(filepath, 'w', encoding='utf-8') as f:
#             f.write(new_content)
#         return f"File '{filename}' updated successfully."
#     except Exception as e:
#         return f"Error updating file: {e}"

# def append_to_file(filename: str, additional_content: str) -> str:
#     """Appends content to the end of an existing file."""
#     filepath = get_file_path(filename)
#     if not os.path.exists(filepath):
#         return f"File '{filename}' does not exist."
#     try:
#         with open(filepath, 'a', encoding='utf-8') as f:
#             f.write("\n" + additional_content)
#         return f"Content appended to '{filename}' successfully."
#     except Exception as e:
#         return f"Error appending to file: {e}"

# def delete_file(filename: str) -> str:
#     """Deletes a file."""
#     filepath = get_file_path(filename)
#     if os.path.exists(filepath):
#         try:
#             os.remove(filepath)
#             return f"File '{filename}' deleted successfully."
#         except Exception as e:
#             return f"Error deleting file: {e}"
#     return f"File '{filename}' does not exist."

# def list_files() -> list:
#     """Lists all files in the Anton_Files directory."""
#     try:
#         files = os.listdir(FILES_DIR)
#         if not files:
#             return []
        
#         file_info = []
#         for filename in files:
#             filepath = get_file_path(filename)
#             size = os.path.getsize(filepath)
#             modified = os.path.getmtime(filepath)
#             file_info.append({
#                 "name": filename,
#                 "size": size,
#                 "path": filepath
#             })
        
#         return file_info
#     except Exception as e:
#         return []

# def process_file_command(user_query: str) -> dict:
#     """
#     Processes file operation commands and returns a response dictionary.
#     """
#     lower_q = user_query.lower().strip()
    
#     if lower_q == "list files":
#         files = list_files()
#         if not files:
#             return {"success": True, "message": "No files found in the Anton_Files directory.", "type": "file_list", "data": []}
#         return {"success": True, "message": "Files retrieved successfully", "type": "file_list", "data": files}
    
#     if lower_q.startswith("create file"):
#         try:
#             parts = user_query.split("with", 1)
#             filename = parts[0].replace("create file", "", 1).strip()
#             if len(parts) > 1:
#                 content_prompt = parts[1].strip()
#                 generation_prompt = f"Write content for a file named '{filename}'. {content_prompt}"
#                 file_content = model.generate_content(generation_prompt).text
#             else:
#                 file_content = ""
                
#             result = create_file(filename, file_content)
#             return {"success": True, "message": result, "type": "file_create", "filename": filename}
#         except Exception as e:
#             return {"success": False, "message": f"Error in create file command: {e}", "type": "error"}
    
#     elif lower_q.startswith("read file"):
#         try:
#             filename = user_query.replace("read file", "", 1).strip()
#             content = read_file(filename)
#             return {"success": True, "message": f"File '{filename}' content retrieved", "type": "file_read", "content": content, "filename": filename}
#         except Exception as e:
#             return {"success": False, "message": f"Error in read file command: {e}", "type": "error"}
    
#     elif lower_q.startswith("update file"):
#         try:
#             parts = user_query.split("with", 1)
#             filename = parts[0].replace("update file", "", 1).strip()
            
#             if len(parts) > 1:
#                 new_content_prompt = parts[1].strip()
#                 generation_prompt = f"Write updated content for a file named '{filename}'. {new_content_prompt}"
#                 new_content = model.generate_content(generation_prompt).text
#             else:
#                 new_content = ""
                
#             result = update_file(filename, new_content)
#             return {"success": True, "message": result, "type": "file_update", "filename": filename}
#         except Exception as e:
#             return {"success": False, "message": f"Error in update file command: {e}", "type": "error"}

#     elif lower_q.startswith("append to file"):
#         try:
#             parts = user_query.split("with", 1)
#             filename = parts[0].replace("append to file", "", 1).strip()
            
#             if len(parts) > 1:
#                 append_content_prompt = parts[1].strip()
#                 generation_prompt = f"Write additional content to append to a file named '{filename}'. {append_content_prompt}"
#                 append_content = model.generate_content(generation_prompt).text
#             else:
#                 append_content = ""
                
#             result = append_to_file(filename, append_content)
#             return {"success": True, "message": result, "type": "file_append", "filename": filename}
#         except Exception as e:
#             return {"success": False, "message": f"Error in append to file command: {e}", "type": "error"}

#     elif lower_q.startswith("delete file"):
#         try:
#             filename = user_query.replace("delete file", "", 1).strip()
#             result = delete_file(filename)
#             return {"success": True, "message": result, "type": "file_delete", "filename": filename}
#         except Exception as e:
#             return {"success": False, "message": f"Error in delete file command: {e}", "type": "error"}

#     return None

# # Initialize Flask app
# app = Flask(__name__)

# # Store chat history
# chat_history = []

# @app.route('/')
# def index():
#     template_path = os.path.join(os.getcwd(), 'templates', 'index.html')
#     print("Looking for template at:", template_path)
#     print("Template exists:", os.path.exists(template_path))
#     return render_template('index.html')

# @app.route('/api/send_message', methods=['POST'])
# def send_message():
#     data = request.json
#     user_message = data.get('message', '')
    
#     if not user_message:
#         return jsonify({"success": False, "message": "No message provided"})
    
#     # Add user message to chat history
#     chat_history.append({"sender": "user", "message": user_message, "timestamp": time.time()})
    
#     # Process file commands
#     file_result = process_file_command(user_message)
    
#     if file_result is not None:
#         chat_history.append({"sender": "anton", "message": file_result["message"], "timestamp": time.time(), "metadata": file_result})
#         return jsonify({
#             "success": True,
#             "response": file_result["message"],
#             "metadata": file_result
#         })
    
#     # Process regular chat message
#     try:
#         response = Antons_Response(user_message)
#         chat_history.append({"sender": "anton", "message": response, "timestamp": time.time()})
#         return jsonify({
#             "success": True,
#             "response": response
#         })
#     except Exception as e:
#         error_message = f"Error processing your message: {str(e)}"
#         chat_history.append({"sender": "anton", "message": error_message, "timestamp": time.time()})
#         return jsonify({
#             "success": False,
#             "response": error_message
#         })
# @app.route('/api/chat_history', methods=['GET'])
# def get_chat_history():
#     return jsonify({
#         "success": True,
#         "history": chat_history
#     })

# @app.route('/api/files', methods=['GET'])
# def get_files():
#     files = list_files()
#     return jsonify({
#         "success": True,
#         "files": files
#     })

# @app.route('/api/file/<filename>', methods=['GET'])
# def get_file_content(filename):
#     content = read_file(filename)
#     return jsonify({
#         "success": True,
#         "filename": filename,
#         "content": content
#     })

# @app.route('/files/<path:filename>')
# def serve_file(filename):
#     return send_from_directory(FILES_DIR, filename)

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)


import os
import subprocess
import sys
from dotenv import load_dotenv
load_dotenv()

# Environment Variables
AiKey = os.getenv("GEMINI_API_KEY")
SearchId = os.getenv("SEARCH_ENGINE_ID")
SearchKey = os.getenv("CUSTOM_SEARCH_KEY")

# Google AI & Search
import google.generativeai as genai
from googleapiclient.discovery import build

# TTS & STT
import pyttsx3
import speech_recognition as sr

# Configure Gemini
genai.configure(api_key=AiKey)
model = genai.GenerativeModel('gemini-2.5-flash-thinking-exp')
chat = model.start_chat(history=[])

# Text-to-Speech
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Speech-to-Text
recognizer = sr.Recognizer()
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError:
        return "Speech recognition service unavailable."

# Search Handling
def Anton_Search(query, num_results=7):
    service = build("customsearch", "v1", developerKey=SearchKey)
    results = service.cse().list(q=query, cx=SearchId, num=num_results).execute()
    search_results = []
    if "items" in results:
        for item in results["items"]:
            search_results.append({
                "title": item["title"],
                "link": item["link"],
                "snippet": item.get("snippet", "")
            })
    return search_results

def Should_Anton_search(user_query):
    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')
    decision_prompt = f"""The user asked: "{user_query}" .
    Determine if you need to search the web for up-to-date information.  
    Respond ONLY with 'yes' or 'no'. If the question involves recent news, real-time events, or changing data, say 'yes'.  
    Otherwise, say 'no'."""
    response = model.generate_content(decision_prompt).text.strip().lower()
    return "yes" in response

def Antons_Response(user_query):
    model = genai.GenerativeModel('gemini-2.5-flash-thinking-exp')
    if Should_Anton_search(user_query):
        search_results = Anton_Search(user_query)
        search_info = "\n".join({
            f"Title: {res['title']}\nURL: {res['link']}\nSnippet: {res['snippet']}\n"
            for res in search_results
        })
        final_prompt = f"""The user asked:"{user_query}"
        Here are relevant Anton's web search results:  
        {search_info}  
        Based on this, generate the best possible answer in a **concise and crux-based manner**. Limit your answer to key takeaways or a brief summary."""
        final_response = model.generate_content(final_prompt).text
    else:
        final_response = model.generate_content(f"Answer the following in a short, crisp, and focused summary: {user_query}").text
    return final_response

# File Management
FILES_DIR = "Anton_Files"
os.makedirs(FILES_DIR, exist_ok=True)

def get_file_path(filename: str) -> str:
    return os.path.join(FILES_DIR, filename)

def create_file(filename: str, content: str) -> str:
    filepath = get_file_path(filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File '{filename}' created at '{filepath}'."
    except Exception as e:
        return f"Error creating file: {e}"

def read_file(filename: str) -> str:
    filepath = get_file_path(filename)
    if not os.path.exists(filepath):
        return f"File '{filename}' does not exist."
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"Content of '{filename}':\n\n{content}"
    except Exception as e:
        return f"Error reading file: {e}"

def update_file(filename: str, new_content: str) -> str:
    filepath = get_file_path(filename)
    if not os.path.exists(filepath):
        return f"File '{filename}' does not exist."
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return f"File '{filename}' updated successfully."
    except Exception as e:
        return f"Error updating file: {e}"

def append_to_file(filename: str, additional_content: str) -> str:
    filepath = get_file_path(filename)
    if not os.path.exists(filepath):
        return f"File '{filename}' does not exist."
    try:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write("\n" + additional_content)
        return f"Content appended to '{filename}' successfully."
    except Exception as e:
        return f"Error appending to file: {e}"

def delete_file(filename: str) -> str:
    filepath = get_file_path(filename)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            return f"File '{filename}' deleted successfully."
        except Exception as e:
            return f"Error deleting file: {e}"
    return f"File '{filename}' does not exist."

def list_files() -> str:
    try:
        files = os.listdir(FILES_DIR)
        if not files:
            return "No files found in the Anton_Files directory."
        file_info = []
        for filename in files:
            filepath = get_file_path(filename)
            size = os.path.getsize(filepath)
            file_info.append(f"{filename} - {size} bytes")
        return "Files in Anton_Files directory:\n" + "\n".join(file_info)
    except Exception as e:
        return f"Error listing files: {e}"

def open_file(filename: str) -> str:
    filepath = get_file_path(filename)
    if not os.path.exists(filepath):
        return f"File '{filename}' does not exist."
    try:
        if filename.endswith(('.cpp', '.py', '.txt', '.html', '.js', '.css')):
            command = f"code \"{filepath}\""
        elif filename.endswith('.pdf'):
            command = f"start \"\" \"{filepath}\"" if os.name == 'nt' else f"xdg-open \"{filepath}\""
        elif filename.endswith(('.docx', '.doc')):
            command = f"start winword \"{filepath}\"" if os.name == 'nt' else f"libreoffice \"{filepath}\""
        else:
            if os.name == 'nt':
                command = f"start \"\" \"{filepath}\""
            else:
                command = f"xdg-open \"{filepath}\""
        subprocess.run(command, shell=True)
        return f"Opening '{filename}'..."
    except Exception as e:
        return f"Error opening file: {e}"

def process_file_command(user_query: str) -> str:
    lower_q = user_query.lower().strip()
    if lower_q == "list files":
        return list_files()
    if lower_q.startswith("create file"):
        try:
            parts = user_query.split("with", 1)
            filename = parts[0].replace("create file", "", 1).strip()
            if len(parts) > 1:
                content_prompt = parts[1].strip()
                generation_prompt = f"Write content for a file named '{filename}'. {content_prompt}"
                file_content = model.generate_content(generation_prompt).text
            else:
                file_content = ""
            return create_file(filename, file_content)
        except Exception as e:
            return f"Error in create file command: {e}"
    elif lower_q.startswith("read file"):
        try:
            filename = user_query.replace("read file", "", 1).strip()
            return read_file(filename)
        except Exception as e:
            return f"Error in read file command: {e}"
    elif lower_q.startswith("update file"):
        try:
            parts = user_query.split("with", 1)
            filename = parts[0].replace("update file", "", 1).strip()
            if len(parts) > 1:
                new_content_prompt = parts[1].strip()
                generation_prompt = f"Write updated content for a file named '{filename}'. {new_content_prompt}"
                new_content = model.generate_content(generation_prompt).text
            else:
                new_content = ""
            return update_file(filename, new_content)
        except Exception as e:
            return f"Error in update file command: {e}"
    elif lower_q.startswith("append to file"):
        try:
            parts = user_query.split("with", 1)
            filename = parts[0].replace("append to file", "", 1).strip()
            if len(parts) > 1:
                append_content_prompt = parts[1].strip()
                generation_prompt = f"Write additional content to append to a file named '{filename}'. {append_content_prompt}"
                append_content = model.generate_content(generation_prompt).text
            else:
                append_content = ""
            return append_to_file(filename, append_content)
        except Exception as e:
            return f"Error in append to file command: {e}"
    elif lower_q.startswith("delete file"):
        try:
            filename = user_query.replace("delete file", "", 1).strip()
            return delete_file(filename)
        except Exception as e:
            return f"Error in delete file command: {e}"
    elif lower_q.startswith("open file"):
        try:
            filename = user_query.replace("open file", "", 1).strip()
            return open_file(filename)
        except Exception as e:
            return f"Error in open file command: {e}"
    return None

# MAIN CHAT LOOP
def main():
    print("Chat with Anton. Type 'exit' to end.")
    print("File operations available:")
    print("  'create file <filename> with <content prompt>'")
    print("  'read file <filename>'")
    print("  'update file <filename> with <content prompt>'")
    print("  'append to file <filename> with <content prompt>'")
    print("  'delete file <filename>'")
    print("  'open file <filename>'")
    print("  'list files'")
    print("--------------------------------------------------------------------------------------------------------------------------------")

    while True:
        mode = input("Type or Talk? (t/s): ").strip().lower()
        if mode == "s":
            user_input = recognize_speech()
            print("You said:", user_input)
        else:
            user_input = input("User: ")
        
        if user_input.lower() in ["exit", "quit", "stop"]:
            print("Goodbye!")
            speak("Goodbye!")
            break
        
        file_command_result = process_file_command(user_input)
        
        if file_command_result is not None:
            print(f"Anton (File Tool): {file_command_result}")
            speak(file_command_result)
        else:
            if user_input.lower() in ["who are you", "who are you ?", "what are you", "what are you ?", "introduce yourself"]:
                response = "I am Anton, your AI assistant. How can I help you today?"
            else:
                response = Antons_Response(user_input)
            print(f"Anton: {response}")
            speak(response)
        
        print("--------------------------------------------------------------------------------------------------------------------------------")

if __name__ == "__main__":
    main()