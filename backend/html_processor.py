import requests
from bs4 import BeautifulSoup
from typing import List, Optional

class HTMLProcessor:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_html(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from the given URL
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch URL: {str(e)}")
    
    def clean_html(self, html_content: str) -> tuple:
        """
        Parse HTML content and return both cleaned text and raw HTML
        """
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Get raw HTML (prettified for readability)
        raw_html = soup.prettify()
        
        # Remove script and style elements for text version
        for script in soup(["script", "style", "meta", "link", "noscript"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text, raw_html
    
    def process_url(self, url: str) -> tuple:
        """
        Fetch and process HTML from URL, return both cleaned text and raw HTML
        """
        try:
            if not url or not isinstance(url, str) or not url.startswith(('http://', 'https://')):
                raise ValueError(f"Invalid URL format: {url}")
                
            html_content = self.fetch_html(url)
            if not html_content:
                raise ValueError("No content returned from URL")
                
            cleaned_text, raw_html = self.clean_html(html_content)
            
            if not cleaned_text or not raw_html:
                raise ValueError("Failed to clean HTML content")
                
            return cleaned_text, raw_html
            
        except Exception as e:
            error_msg = f"Error processing URL {url}: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)