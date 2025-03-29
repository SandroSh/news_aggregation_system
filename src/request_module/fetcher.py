import requests.exceptions
from requests_html import HTMLSession
from contextlib import closing
import logging
from typing import Optional
import time

def fetch_webpage(url:str, render_js : bool= False, timeout: int = 19, max_retires: int = 3, retry_delay: int = 2) -> Optional[str]:
    
    """
    Safely fetches the HTML content of a webpage with retry mechanism and proper resource cleanup.
    
    Args:
        url (str): The URL of the webpage to fetch
        render_js (bool): Whether to render JavaScript (default: False)
        timeout (int): Timeout in seconds for rendering (default: 19)
        max_retries (int): Maximum number of retry attempts (default: 3)
        retry_delay (int): Delay between retries in seconds (default: 2)
    
    Returns:
        Optional[str]: The HTML content of the page as a string, or None if the request fails
    
    Raises:
        ValueError: If the URL is invalid or empty
    """
    
    if not url or not url.strip():
        raise ValueError('URL must be a non-empty string')
    
    if not url.startswith(('http://', 'https://')):
        url = f'https://{url}'
    
    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger(__name__)
    
    attempt = 0
    html_content = None
    
    while attempt < max_retires:
        
        with closing(HTMLSession()) as session:
            
            try:
                response = session.get(url, timeout = timeout)
                
                response.raise_for_status()
                
                if render_js:
                    time.sleep(1)
                    
                    response.html.render(timeout = timeout, keep_page = True, scrolldown = 1)
                
                html_content = response.html.html
                break
            except Exception as e:
                attempt += 1
                error_message = f"Attempt {attempt}:{max_retires} failed: {str(e)}"
                logger.warning(error_message)
                
                if attempt == max_retires:
                    logger.error(f"All attempts failed for URL: {url}")
                    return None
            except KeyboardInterrupt:
                logger.info("Request interrupted by user")
                return None
    return html_content
                