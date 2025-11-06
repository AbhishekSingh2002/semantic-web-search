export default function ResultsList({ results, url, query, totalChunks }) {
  // Debug logging
  console.log('ResultsList props:', { results, url, query, totalChunks });
  
  if (!results || results.length === 0) {
    return (
      <div className="no-results">
        <h3>No results found</h3>
        <p>Try adjusting your search query or URL</p>
      </div>
    );
  }

  return (
    <div>
      <div className="results-header">
        <h2>Search Results</h2>
        <p>
          Found {results.length} relevant chunks out of {totalChunks} total chunks from{' '}
          <strong>{url}</strong>
        </p>
        <p style={{ marginTop: '0.5rem' }}>
          Query: <strong>"{query}"</strong>
        </p>
      </div>

      <div className="results-list">
        {results.map((result, index) => (
          <div key={result.chunk_id || index} className="result-card">
            <div className="result-header">
              <span className="result-rank">#{index + 1}</span>
              <div className="result-meta">
                <div className="meta-item">
                  <span>📝 {result.token_count} tokens</span>
                </div>
                <div className="meta-item">
                  <span className="score-badge">
                    {(result.relevance_score * 100).toFixed(1)}% match
                  </span>
                </div>
              </div>
            </div>
            <div className="result-content">
              {result.content}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}