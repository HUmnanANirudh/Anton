import os
from dotenv import load_dotenv
load_dotenv() 
Key = os.getenv("GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=Key)
prompt = "Explain the concept of Occam's Razor and provide a simple, everyday example."
response = client.models.generate_content(
    model="gemini-2.0-flash-thinking-exp",  
    contents=prompt
)
print(response.text)