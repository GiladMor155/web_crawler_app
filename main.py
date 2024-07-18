import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

def get_page_content(url):
    """Fetches the content of the page at the given URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure we notice bad responses
    return response.text

def extract_info(url):
    """Extracts page name, URL, and main text content from a given URL."""
    page_content = get_page_content(url)
    soup = BeautifulSoup(page_content, 'html.parser')

    page_title = soup.title.string if soup.title else 'No title'
    main_text = ' '.join(p.text for p in soup.find_all('p'))

    return {
        'שם דף': page_title,
        'כתובת עמוד': url,
        'תוכן עמוד': main_text
    }

def web_crawler(start_url):
    """Performs web crawling starting from the given URL, extracting data from the main page and its first-level links."""
    main_page_info = extract_info(start_url)
    page_links = [start_url]

    soup = BeautifulSoup(get_page_content(start_url), 'html.parser')
    for link in soup.find_all('a', href=True):
        full_url = urljoin(start_url, link['href'])
        if full_url not in page_links and len(page_links) < 11:  # Limiting to 10 additional links
            page_links.append(full_url)

    all_page_info = [extract_info(url) for url in page_links]

    return all_page_info

def save_to_excel(data, filename):
    """Saves the extracted data to an Excel file."""
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

# Example usage:
start_url = 'https://www.artificialintelligence-news.com/'  # Replace with the actual start URL of AI News site
crawled_data = web_crawler(start_url)
save_to_excel(crawled_data, 'web_crawl_results.xlsx')

print("Data has been saved to 'web_crawl_results.xlsx'")
