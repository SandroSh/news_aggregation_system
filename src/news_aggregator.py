from bs4 import BeautifulSoup


def parse_html(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    else:
        print("No HTML content to parse.")
        return None