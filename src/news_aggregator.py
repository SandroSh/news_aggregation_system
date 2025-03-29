from datetime import datetime
import logging
import os
from typing import Dict, List
from bs4 import BeautifulSoup

from request_module import fetch_webpage
from utils import absolute_url

def parse_html(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    else:
        print("No HTML content to parse.")
        return None
    
def extract_headlines_with_urls(html_content:str, log_dir:str = 'logs', url:str = '') -> List[Dict[str,str]]:
    """
    Extracts headlines and their associated URLs from HTML content using BeautifulSoup.
    
    Args:
        html_content (str): The HTML content to parse
        log_dir (str): Directory to store log files (default: "logs")
        
    Returns:
        List[Dict[str, str]]: List of dictionaries containing headline text and URL
                             Each dict has 'headline' and 'url' keys
    """
    os.makedirs(log_dir, exist_ok = True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"headlines_extraction_{timestamp}.log")
    
    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s - %(levelname)s - %(message)s',
        handlers= [logging.FileHandler(log_file)]
    )
    logger = logging.getLogger(__name__);
    
    results = []
    
    try:
        if not html_content or not isinstance(html_content, str):
            logger.error("Invalid HTML content provided")
            return results
        
        soup = parse_html(html_content=html_content)
        
        headline_tags = ['h1', 'h2', 'h3']
        
        for tag in headline_tags:
            news = soup.find_all(tag)
            
            if not news:
                tags = soup.find_all('a')
                for tag in tags: 
                    if len(tag.get_text().strip()) > 35: 
                        news.append(tag)
                
            
            for headline in news:
                link = None
                time = None
         
                if headline.find_parent('a'):
                    link = headline.find_parent('a')
                elif headline.find('a'):
                    link = headline.find('a')
                else:
                    parent = headline.find_parent()
                    
                    for _ in range(3):
                        if parent and parent.find('a'):
                            link = parent.find('a') 
                            break
                        parent = parent.find_parent() if parent else None
                        
                if link and link.get('href'):
                    headline_text = headline.get_text(strip = True)
                    
                    if headline_text:
                        # print(headline_text)
                        time_tag = headline.find_next('time')
                        
                        if not time_tag:
                            time_tag = link.find_next('time')
                        
                        if not time_tag:
                            parent = headline.find_parent()
                            time_tag = parent.find('time') if parent else None
                            
                            
                        time = time_tag.get('datetime') if time_tag else None    
                            
                        result = {
                            'headline': headline_text,
                            'url': absolute_url(url, link['href']),
                            'date': time  
                        }
                        
                        results.append(result)
                        
                        # logger.info(f"Found headline: {headline_text} with URL: {link['href']}")
            
        if not results:
            logger.warning("No headlines  with urls found in the content")
        else:
            logger.info(F'Succesfully extracted {len(results)} headlines with urls')  
            return results      
                
                
    except Exception as e:
        logger.error(f"Error processing HTML content {e}")
        return results
    
    

    
        
    
    
if __name__ == "__main__":
    url_ipn = "https://www.interpressnews.ge"
    url_sazmau = "https://1tv.ge/sporti/siakhleebi/"
    
    html_content_ipn = fetch_webpage(url_ipn)
    html_content_sazmau = fetch_webpage(url_sazmau)
    news_data_ipn  = extract_headlines_with_urls(html_content_ipn, url=url_ipn)
    news_data_sazmau  = extract_headlines_with_urls(html_content_sazmau)
    
    news_data_ipn.extend(news_data_sazmau)

    data = news_data_ipn
    
   
    
  
