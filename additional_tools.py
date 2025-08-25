import csv
import os

from bs4 import BeautifulSoup as bs 
import requests
from groq import Groq
import json
from api_key import API_KEY, openrouter_api, google_gemini_api_key
from ollama import chat
from ollama import ChatResponse
import ollama
from openai import OpenAI
from google import genai
from google.genai import types

# genai.configure(api_key=google_gemini_api_key)

class open_router_classifier:
    def __init__(self):
        self.client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api,
        )
    
    def classify(self, data):
        completion = self.client.chat.completions.create(
        model="tencent/hunyuan-a13b-instruct:free",
        # model="moonshotai/kimi-k2:free",
        messages=[
            {"role": "system", "content": f'{default_prompt} '},
            {
            "role": "user",
            "content": str(data)
            }
        ]
        )
        print(f"\nClassified as:{completion.choices[0].message.content}\n")
        response = completion.choices[0].message.content
        response = response.split('>')[1].split('</')[0].strip()
        return response
    
class groq_classifier:
    def __init__(self):
        self.client = Groq(
            api_key=API_KEY
        )

    def classify(self, data):
        """Uses AI to extract food items, price range, and intent from the user's query."""
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": f'{default_prompt} '},
                {"role": 'user', "content": str(data)}
            ],
            model="openai/gpt-oss-20b",
            # reasoning_format="parsed",
            temperature=0.30,
            # response_format={'type':'json_object'}
        )
        
        response = chat_completion.choices[0].message.content.strip()
        print(f"\nClassified as:{response}\n")
        return response
    
class ollama_local():
    def __init__(self):
        self.client = ollama.Client()
        
    def classify(self, data):
        response = self.client.generate(model='instagram_reel_classifier', prompt=data)
        print(f"\nClassified as:{response.response}\n")
        return response.response

class google_gemini():
    def __init__(self):
        self.generation_config = types.GenerateContentConfig(
        system_instruction=default_prompt,
        temperature=0.7   # Adjust as needed
        )

        self.gemini_client = genai.Client()

    
    def classify(self, data):
        response = self.gemini_client.models.generate_content(
        model="gemini-2.5-flash-lite",        # Or "gemini-2.0-flash" etc.
        config=self.generation_config,
        contents=str(data)
    )
        print(f"\nClassified as:{response.text}\n")
        return response.text



default_prompt = """
i am trying to build a modal that will take an instagram video as input and tell what type of content that reel is all about, like either it's entertainment, education, love, health etc.

So i will provide you with captions, titles and comments of the reel and you have to tell which of the following category is best suited for that reel -

*Entertainment (memes, funny, jokes, movies)

*music

*health

*motivation

*emotional

*informational

*shopping

consider the comments provided to rethink if the reel is either informational or not, since the captions can be manipulated to trick algorithms. so consider the comments as well.
please always respond with just one word, that will be the name of the category you think the reel is of
AGAIN, PLEASE ONLY REPLY WIH JUST ONE WORD
And also don't priortise travel reels, since they are also a kind of entertainment, so don't classify them as informational, they are a travel category.
here is the caption of the reel - 
"""     

def send_ai_request(data, comments=None):
    # response = requests.post('http://localhost:3000/chat',json={'message':f'{default_prompt}{data}'})
    reel_data = {'caption':data, 'comments':comments}
    # response = ask_gemini(str(reel_data))
    gemini = google_gemini()
    response = gemini.classify(str(reel_data))
    print(f'\nAI RESPONSE: {response}\n')
    quit()
    save_to_json({'caption':data, 'comments':comments, 'target':response})
    save_reel_to_csv(data, comments, response )
    return response

def save_to_json(data):
    filename = 'reels_data.json'
    # Read existing data
    if os.path.isfile(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Append new data
    existing_data.append(data)

    # Save back to file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, indent=4)
    print(f'\nSAVED DATA TO JSON: {data["caption"]}\n')


def save_reel_to_csv(caption, comments, category, filename='classified_reels.csv'):
    # Ensure comments is a string (e.g., joined by newlines or commas)
    if isinstance(comments, list):
        comments = "\n".join(comments)

    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header if file doesn't exist
        if not file_exists:
            writer.writerow(["caption", "comments", "category"])

        # Write the data
        writer.writerow([caption, comments, category])
