# Semantic Web Search Engine

A semantic search engine that allows users to search through HTML content of web pages using natural language queries. The application fetches web pages, processes the HTML content, and performs semantic search to find the most relevant content chunks.

## Features

- **Web Page Crawling**: Fetches and parses HTML content from any public URL
- **Semantic Search**: Uses vector embeddings to understand the meaning behind search queries
- **Content Chunking**: Splits web pages into manageable chunks for efficient searching
- **Relevance Ranking**: Ranks search results based on semantic similarity
- **Modern Web Interface**: Clean, responsive UI built with Next.js

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- pip (Python package manager)

## Project Structure

```
semantic-web-search/
├── backend/               # Flask backend
│   ├── app.py            # Main application
│   ├── html_processor.py # HTML processing logic
│   ├── tokenizer.py      # Text tokenization
│   ├── vector_store.py   # Vector database operations
│   ├── schemas.py        # Pydantic models
│   └── requirements.txt  # Python dependencies
├── frontend/             # Next.js frontend
│   ├── components/       # React components
│   ├── pages/            # Next.js pages
│   ├── styles/           # CSS modules
│   ├── package.json      # Frontend dependencies
│   └── next.config.js    # Next.js configuration
└── README.md             # This file
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```bash
   python app.py
   ```
   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   The frontend will be available at `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Enter a URL you want to search in the first input field
3. Enter your search query in the second input field
4. Click the "Search" button
5. View the relevant content chunks from the webpage

## Vector Database Configuration

This project uses ChromaDB as the vector database, which runs in-memory by default. No additional setup is required for local development.

### Configuration Options

You can modify the vector database settings in `backend/vector_store.py`:

```python
# Default configuration
CHUNK_SIZE = 500  # Maximum tokens per chunk
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"  # Embedding model
```

## Environment Variables

### Backend

Create a `.env` file in the backend directory with the following variables:

```
FLASK_APP=app.py
FLASK_ENV=development
BACKEND_URL=http://localhost:5000
```

### Frontend

Create a `.env.local` file in the frontend directory with the following variables:

```
NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
```

## Testing

To run the backend tests:

```bash
cd backend
python -m pytest
```

## Deployment

### Backend

For production deployment, consider using:
- Gunicorn or uWSGI as the WSGI server
- Nginx as a reverse proxy
- Environment variables for configuration

Example Gunicorn command:
```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

### Frontend

Build the production version:
```bash
cd frontend
npm run build
npm start
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - Backend web framework
- [Next.js](https://nextjs.org/) - React framework
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Sentence Transformers](https://www.sbert.net/) - For generating embeddings
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
