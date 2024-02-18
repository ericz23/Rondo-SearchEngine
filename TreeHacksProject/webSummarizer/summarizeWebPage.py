import requests  
import pandas as pd  
from bs4 import BeautifulSoup  
from openai import OpenAI
from dotenv import load_dotenv
import os
  

load_dotenv('openAI.env')
#secret_key = os.getenv("OPENAI_KEY")
secret_key = "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"


def getdata(url):  
    """
    Uses BeautifulSoup to extract the text data from webpage
    :param url: The URL of the webpage to extract data from
    :return: The text data from the webpage
    :raises ValueError: If there is no textual data that can be extracted using this method
    """
    r = requests.get(url)  
    soup = BeautifulSoup(r.text, 'html.parser')
    string = ""
    for data in soup.find_all("p"):
        string += data.get_text()
    if string == "":
        raise ValueError("No textual data to extract")
    return string 

def wordCap(string, cap):
    """
    Caps the number of words in a string (to lessen token usage)
    :param string: The string to be capped
    :param cap: The number of words to cap the string at
    :return: The capped string
    """
    return " ".join(string.split()[:cap])


def summarize(webpage_Data):
    """
    Uses OpenAI's GPT-3.5 model to summarize the webpage data and return a summary of the webpage
    :param webpage_Data: The data from the webpage to be summarized
    :return: A summary of the webpage data
    :raises ValueError: If the webpage data is too short to summarize
    """
    if len(webpage_Data) < 100:
        raise ValueError("Webpage data is too short to summarize")
    webpage_Data = wordCap(webpage_Data, 450)
    data = {
        "model": "gpt-3.5-turbo-0125",  
        "messages": [
            {"role": "system", "content": "You are an assistant tasked with helping elderly people utilize the internet in their daily lives. Your job is to summarize the following webpage and tell the user in a friendly way what they can find on the website so that they can figure out which site is best for what they are looking for. Keep your response under 100 words."},
            {"role": "user", "content": webpage_Data},
        ],
        "max_tokens": 200,  
        "temperature": 0.7  
    }

    
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json"
    }

    endpoint = "https://api.openai.com/v1/chat/completions"
    response = requests.post(endpoint, json=data, headers=headers)

    
    if response.status_code == 200:

        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error: something went wrong"

test1 = "https://www.cbc.ca/life/culture/the-best-card-games-to-play-with-a-standard-deck-1.5836447"
test2 = "https://www.rollingstone.com/tv-movies/tv-movie-news/how-to-watch-downton-abbey-series-movie-free-online-1356705/"
test3 = "https://www.cbc.ca/news/canada/london/london-pastor-lacks-funds-but-not-faith-in-building-black-community-centre-1.5836446"
tests = [test1, test2, test3]

for test in tests:
    string = getdata(test)  
    helper = summarize(string)
    print(helper)

