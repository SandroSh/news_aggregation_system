import requests.exceptions
import requests
from bs4 import BeautifulSoup

def fetch_webpage(url:str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        
    except requests.exceptions.RequestException as e:
        print(f'Error in fetching page {e}')
        return None