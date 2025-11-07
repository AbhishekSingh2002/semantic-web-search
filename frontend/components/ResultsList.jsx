import { useState } from 'react';

export default function ResultsList({ results, url, query, totalChunks }) {
  const [expandedResults, setExpandedResults] = useState({});

  console.log('ResultsList props:', { results, url, query, totalChunks });
  
  if (!results || results.length === 0) {
    return (
      <div className="no-results">
        <h3>No results found</h3>
        <p>Try adjusting your search query or URL</p>
      </div>
    );
  }

  const toggleHtml = (index) => {
    setExpandedResults(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  return (
    <div>
      <div className="results-header">
        <h2>Search Results</h2>
      </div>

      <div className="results-list">
        {results.map((result, index) => (
          <div key={result.chunk_id || index} className="result-card">
            <div className="result-header">
              <div className="result-title">
                {result.content.substring(0, 100)}...
              </div>
              <span className="score-badge">
                {(result.relevance_score * 100).toFixed(0)}% match
              </span>
            </div>
            
            <div className="result-path">
              Path: /home
            </div>

            <button 
              className="view-html-btn"
              onClick={() => toggleHtml(index)}
            >
              <span>{expandedResults[index] ? '◆' : '◇'}</span>
              View HTML {expandedResults[index] ? '▲' : '▼'}
            </button>

            {expandedResults[index] && (
              <div className="html-content">
                {result.html || result.content}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}