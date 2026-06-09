import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import uuid

class VectorStore:
    def __init__(self, collection_name: str = "html_chunks"):
        """
        Initialize ChromaDB vector store with sentence transformers
        """
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))
        
        # Use sentence transformer for embeddings
        # Lazy load model on first use
        self.model = None
        
        # Create or get collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            # Clear existing data for fresh indexing
            self.client.delete_collection(name=collection_name)
        except:
            pass
        
        self.collection = self.client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def _get_model(self):
        """Lazy load the sentence transformer model"""
        if self.model is None:
            self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        return self.model

    def add_chunks(self, chunks: List[dict], url: str) -> None:
        """
        Add text chunks to the vector store
        """
        if not chunks:
            return
        
        texts = [chunk['text'] for chunk in chunks]
        token_counts = [chunk['token_count'] for chunk in chunks]
        
        # Generate embeddings
        embeddings = self._get_model().encode(texts, show_progress_bar=False)
        
        # Prepare data for ChromaDB
        ids = [f"{url}_{i}_{uuid.uuid4().hex[:8]}" for i in range(len(chunks))]
        metadatas = [
            {
                'url': url,
                'token_count': token_counts[i],
                'chunk_index': i
            }
            for i in range(len(chunks))
        ]
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Search for relevant chunks using semantic similarity
        """
        # Generate query embedding
        query_embedding = self._get_model().encode([query], show_progress_bar=False)[0]
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=min(top_k, self.collection.count())
        )
        
        # Format results
        search_results = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                search_results.append({
                    'content': results['documents'][0][i],
                    'token_count': results['metadatas'][0][i]['token_count'],
                    'relevance_score': float(1 - results['distances'][0][i]),  # Convert distance to similarity
                    'chunk_id': results['ids'][0][i]
                })
        
        return search_results
    
    def clear(self) -> None:
        """
        Clear all data from the collection
        """
        try:
            self.client.delete_collection(name=self.collection.name)
            self.collection = self.client.create_collection(
                name=self.collection.name,
                metadata={"hnsw:space": "cosine"}
            )
        except:
            pass