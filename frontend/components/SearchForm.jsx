import { useState } from 'react';

export default function SearchForm({ onSearch, loading }) {
  const [url, setUrl] = useState('');
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url && query) {
      onSearch({ url, query });
    }
  };

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <span className="input-icon">🌐</span>
        <input
          id="url"
          type="url"
          placeholder="https://smarter.codes"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <span className="input-icon">🔍</span>
        <input
          id="query"
          type="text"
          placeholder="AI"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          required
          disabled={loading}
        />
      </div>

      <button 
        type="submit" 
        className="submit-btn"
        disabled={loading || !url || !query}
      >
        {loading ? (
          <>
            <span className="spinner" style={{ width: '16px', height: '16px', borderWidth: '2px' }}></span>
            Searching...
          </>
        ) : (
          <>
            <span>🔍</span>
            Search
          </>
        )}
      </button>
    </form>
  );
}