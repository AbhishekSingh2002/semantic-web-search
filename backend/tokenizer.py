from transformers import AutoTokenizer
from typing import List

class ContentTokenizer:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize tokenizer with a pretrained model
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.max_tokens = 500
    
    def tokenize(self, text: str) -> List[int]:
        """
        Tokenize text into token IDs
        """
        return self.tokenizer.encode(text, add_special_tokens=True)
    
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in text
        """
        return len(self.tokenize(text))
    
    def chunk_text(self, text: str, raw_html: str, max_tokens: int = 500, overlap: int = 50) -> List[dict]:
        """
        Split text into chunks with maximum token count
        Also extract corresponding HTML snippets
        Returns list of dicts with chunk text, HTML snippet, and token count
        """
        # Split text into sentences (simple approach)
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        sentences = [s.strip() + '.' for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = []
        current_tokens = 0
        char_position = 0
        
        for sentence in sentences:
            sentence_tokens = self.count_tokens(sentence)
            
            # If single sentence exceeds max_tokens, split it by words
            if sentence_tokens > max_tokens:
                words = sentence.split()
                word_chunk = []
                
                for word in words:
                    word_token_count = self.count_tokens(' '.join(word_chunk + [word]))
                    if word_token_count > max_tokens and word_chunk:
                        chunk_text = ' '.join(word_chunk)
                        html_snippet = self._extract_html_snippet(raw_html, chunk_text)
                        chunks.append({
                            'text': chunk_text,
                            'html': html_snippet,
                            'token_count': self.count_tokens(chunk_text)
                        })
                        # Keep overlap
                        word_chunk = word_chunk[-overlap:] if len(word_chunk) > overlap else []
                    word_chunk.append(word)
                
                if word_chunk:
                    chunk_text = ' '.join(word_chunk)
                    html_snippet = self._extract_html_snippet(raw_html, chunk_text)
                    chunks.append({
                        'text': chunk_text,
                        'html': html_snippet,
                        'token_count': self.count_tokens(chunk_text)
                    })
                continue
            
            # Check if adding this sentence would exceed max_tokens
            test_chunk = current_chunk + [sentence]
            test_text = ' '.join(test_chunk)
            test_tokens = self.count_tokens(test_text)
            
            if test_tokens > max_tokens and current_chunk:
                # Save current chunk
                chunk_text = ' '.join(current_chunk)
                # Extract a snippet of HTML (approximate)
                html_snippet = self._extract_html_snippet(raw_html, chunk_text)
                chunks.append({
                    'text': chunk_text,
                    'html': html_snippet,
                    'token_count': self.count_tokens(chunk_text)
                })
                
                # Start new chunk with overlap
                overlap_sentences = current_chunk[-2:] if len(current_chunk) > 2 else current_chunk
                current_chunk = overlap_sentences + [sentence]
            else:
                current_chunk.append(sentence)
        
        # Add the last chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            html_snippet = self._extract_html_snippet(raw_html, chunk_text)
            chunks.append({
                'text': chunk_text,
                'html': html_snippet,
                'token_count': self.count_tokens(chunk_text)
            })
        
        return chunks
    
    def _extract_html_snippet(self, raw_html: str, text_chunk: str) -> str:
        """
        Extract a relevant HTML snippet based on text content
        """
        if not raw_html:
            return "No HTML content available"
            
        try:
            # Try to find the position of the text_chunk in the HTML
            if text_chunk and len(text_chunk) > 20:  # Only if we have enough text to search for
                # Get the first 100 chars of the chunk to search for
                search_text = text_chunk[:100]
                pos = raw_html.find(search_text)
                if pos > 0:
                    # Get 1000 chars before and after the found position
                    start = max(0, pos - 1000)
                    end = min(len(raw_html), pos + len(search_text) + 1000)
                    return raw_html[start:end]
            
            # Fallback: return first 2000 chars with proper HTML tags
            if '<body' in raw_html and '</body>' in raw_html:
                body_start = raw_html.find('<body')
                body_end = raw_html.find('</body>') + 7  # +7 to include </body>
                body_content = raw_html[body_start:body_end]
                return body_content[:4000] + ('...' if len(body_content) > 4000 else '')
                
            # Fallback: return first 2000 chars
            return raw_html[:4000] + ('...' if len(raw_html) > 4000 else '')
            
        except Exception as e:
            # Last resort fallback
            return raw_html[:4000] + ('...' if len(raw_html) > 4000 else '')