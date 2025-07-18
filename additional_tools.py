from bs4 import BeautifulSoup as bs 
import requests
from groq import Groq
import json
from api_key import API_KEY

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
here is the caption of the reel - 
"""

def parse_caption_tag(data):
    # with open('index.html','r')as file:
    #     data = file.read()

    soup = bs(data,'html.parser')

    reel = {}

    all_span_tags = soup.find_all('span')
    divs = soup.find_all("div", class_="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xw7yly9 x1uhb9sk xw2csxc x1odjw0f x1c4vz4f xs83m0k xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1")
    reel['caption'] = divs[0].text
    all_a_tags = soup.find_all('a')
    tags = []
    for tag in all_a_tags:
        if tag.text.startswith('Audio') or tag.text.startswith('Tagged'):
            pass
        else:
            tags.append(tag.text)

    reel['tags'] = tags

    return reel

client = Groq(
    api_key=API_KEY
)

def query_ai(data):
    """Uses AI to extract food items, price range, and intent from the user's query."""
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": f'{default_prompt} '},
            {"role": 'user', "content": str(data)}
        ],
        model="deepseek-r1-distill-llama-70b",
        reasoning_format="parsed",
        temperature=0.50,
        # response_format={'type':'json_object'}
    )
    
    response = chat_completion.choices[0].message.content.strip()
    
    # try:
    return response  # Convert AI response to dictionary
    # except json.JSONDecodeError:
    #     print("AI Response Error:", response)
    #     return None

def send_ai_request(data, comments=None):
    # response = requests.post('http://localhost:3000/chat',json={'message':f'{default_prompt}{data}'})
    reel_data = {'caption':data, 'comments':comments}
    response = query_ai(reel_data)
    return response