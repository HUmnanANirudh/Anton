import os
from dotenv import load_dotenv
load_dotenv() 
AiKey = os.getenv("GEMINI_API_KEY")
SearchId = os.getenv("SEARCH_ENGINE_ID")
SearchKey = os.getenv("CUSTOM_SEARCH_KEY")

from google import genai
import google.generativeai as genai
from googleapiclient.discovery import build

genai.configure(api_key=AiKey)
model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')

chat = model.start_chat(history=[])

def Anton_Search(query,num_results=7):
    service = build("customsearch","v1",developerKey=SearchKey)
    results = service.cse().list(q=query,cx=SearchId,num=num_results).execute()

    serach_results = []
    if "items" in results:
        for item in results["items"]:
            serach_results.append({
                "title":item["title"],
                "link":item["link"],
                "snippet": item.get("snippet", "")
            })
    return serach_results

def Should_Anton_search(user_query):
    model= genai.GenerativeModel('gemini-2.0-flash-thinking-exp')
    decision_prompt = f"""The user asked: "{user_query}" .
    Determine if you need to search the web for up-to-date information.  
    Respond ONLY with 'yes' or 'no'. If the question involves recent news, real-time events, or changing data, say 'yes'.  
    Otherwise, say 'no'."""
    response = model.generate_content(decision_prompt).text.strip().lower()
    return "yes" in response

def Antons_Response(user_query):
    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')

    if Should_Anton_search(user_query):
        search_results=Anton_Search(user_query)
        search_info = "\n".join({
            f"Title: {res['title']}\nURL: {res['link']}\nSnippet: {res['snippet']}\n"
            for res in search_results
        }) 
        final_prompt = f"""The user asked:"{user_query}" 
        Here are relevant Anoton's web search results:  
        {search_info}  
        Based on this, generate the best possible answer."""

        final_response = model.generate_content(final_prompt).text
    else:
        final_response = model.generate_content(user_query).text

    return final_response


print("Chat with the Anton. Type 'stop' to end.")

while True:
    user_input = input("User: ")
    if user_input.lower() == "stop":
        break

    response = Antons_Response(user_input)
    print(f"Anton: {response}")
    print("-----------------------------------------------------------------------------------------------------------------------------------------")