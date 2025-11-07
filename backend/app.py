import chromadb
# Disable ChromaDB telemetry to avoid capture() errors
chromadb.telemetry = None

from flask import Flask, request, jsonify
from flask_cors import CORS
from html_processor import HTMLProcessor
from tokenizer import ContentTokenizer
from vector_store import VectorStore
from schemas import SearchRequest, SearchResponse, SearchResult
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize components
html_processor = HTMLProcessor()
tokenizer = ContentTokenizer()
vector_store = VectorStore()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/api/search', methods=['POST'])
def search():
    """
    Main endpoint for searching HTML content
    Expects JSON: {"url": "https://example.com", "query": "search term"}
    """
    try:
        # Parse request
        data = request.get_json()
        
        if not data or 'url' not in data or 'query' not in data:
            return jsonify({
                "error": "Missing required fields: url and query"
            }), 400
        
        search_request = SearchRequest(**data)
        logger.info(f"Processing search request for URL: {search_request.url}")
        
        # Step 1: Fetch and clean HTML
        logger.info("Fetching and cleaning HTML content...")
        cleaned_text, raw_html = html_processor.process_url(search_request.url)
        
        if not cleaned_text or not raw_html:
            return jsonify({
                "error": "No content found at the provided URL"
            }), 400
        
        logger.info(f"Extracted {len(cleaned_text)} characters of text")
        
        # Step 2: Tokenize and chunk the content
        logger.info("Tokenizing and chunking content...")
        chunks = tokenizer.chunk_text(cleaned_text, raw_html, max_tokens=500)
        
        if not chunks:
            return jsonify({
                "error": "Failed to create chunks from content"
            }), 400
        
        logger.info(f"Created {len(chunks)} chunks")
        
        # Step 3: Index chunks in vector store
        logger.info("Indexing chunks in vector store...")
        vector_store.clear()  # Clear previous data
        vector_store.add_chunks(chunks, search_request.url)
        
        # Step 4: Search for relevant chunks
        logger.info(f"Searching for query: {search_request.query}")
        search_results = vector_store.search(search_request.query, top_k=10)
        
        # Step 5: Format response
        results = [
            SearchResult(
                content=result['content'],
                token_count=result['token_count'],
                relevance_score=result['relevance_score'],
                chunk_id=result['chunk_id']
            )
            for result in search_results
        ]
        
        response = SearchResponse(
            results=results,
            total_chunks=len(chunks),
            url=search_request.url,
            query=search_request.query
        )
        
        logger.info(f"Returning {len(results)} results")
        return jsonify(response.model_dump()), 200
        
    except Exception as e:
        error_msg = f"Error processing search request: {str(e)}"
        logger.error(error_msg, exc_info=True)  # This will log the full traceback
        return jsonify({
            "error": "Error processing your request",
            "details": str(e),
            "status": "error"
        }), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    """Get statistics about the current vector store"""
    try:
        count = vector_store.collection.count()
        return jsonify({
            "indexed_chunks": count
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)