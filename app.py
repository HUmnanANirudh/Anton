import os
from dotenv import load_dotenv
load_dotenv() 
Key = os.getenv("GEMINI_API_KEY")

from google import genai
import google.generativeai as genai
try:
    print(genai.GenerativeModel)
except AttributeError:
    print("GenerativeModel not found.")
model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')

chat = model.start_chat(history=[])

def generate_response(user_input):
    try:
        response = chat.send_message(user_input)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"
    
print("Chat with the Gemini agent. Type 'stop' to end.")

while True:
    user_input = input("User: ")
    if user_input.lower() == "stop":
        break

    agent_response = generate_response(user_input)
    print(f"Agent: {agent_response}")
    print("-------------------------------------")