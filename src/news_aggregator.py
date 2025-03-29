from bs4 import BeautifulSoup
from request_module import fetch_webpage

def parse_html(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    else:
        print("No HTML content to parse.")
        return None
    
    
    
if __name__ == "__main__":
    url = "https://www.interpressnews.ge/ka/"
    
    html_content = fetch_webpage(url)
    
    soup = parse_html(html_content)
    if soup:
        
        news_titles = soup.find_all('h2', {'itemprop':'name'})
        news_list = []
        print(news_titles)
        if news_titles:
            for title in news_titles:
                # print(title)
                if title:
                    news_list.append(title.text.strip())

        for item in news_list:
            print(item)
  
    else:
        print("Failed to retrieve or parse the webpage.")