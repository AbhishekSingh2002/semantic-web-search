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
    
    def chunk_text(self, text: str, max_tokens: int = 500, overlap: int = 50) -> List[dict]:
        """
        Split text into chunks with maximum token count
        Returns list of dicts with chunk text and token count
        """
        # Split text into sentences (simple approach)
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        sentences = [s.strip() + '.' for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for sentence in sentences:
            sentence_tokens = self.count_tokens(sentence)
            
            # If single sentence exceeds max_tokens, split it by words
            if sentence_tokens > max_tokens:
                words = sentence.split()
                word_chunk = []
                word_tokens = 0
                
                for word in words:
                    word_token_count = self.count_tokens(' '.join(word_chunk + [word]))
                    if word_token_count > max_tokens and word_chunk:
                        chunk_text = ' '.join(word_chunk)
                        chunks.append({
                            'text': chunk_text,
                            'token_count': self.count_tokens(chunk_text)
                        })
                        # Keep overlap
                        word_chunk = word_chunk[-overlap:] if len(word_chunk) > overlap else []
                    word_chunk.append(word)
                
                if word_chunk:
                    chunk_text = ' '.join(word_chunk)
                    chunks.append({
                        'text': chunk_text,
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
                chunks.append({
                    'text': chunk_text,
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
            chunks.append({
                'text': chunk_text,
                'token_count': self.count_tokens(chunk_text)
            })
        
        return chunks