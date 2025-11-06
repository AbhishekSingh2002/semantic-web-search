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
    
    def clean_html(self, html_content: str) -> str:
        """
        Parse and clean HTML content, removing scripts, styles, and extracting text
        """
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Remove script and style elements
        for script in soup(["script", "style", "meta", "link", "noscript"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def process_url(self, url: str) -> str:
        """
        Fetch and process HTML from URL
        """
        html_content = self.fetch_html(url)
        cleaned_text = self.clean_html(html_content)
        return cleaned_text