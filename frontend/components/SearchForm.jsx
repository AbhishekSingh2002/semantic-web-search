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
        <label htmlFor="url">Website URL</label>
        <input
          id="url"
          type="url"
          placeholder="https://example.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="query">Search Query</label>
        <input
          id="query"
          type="text"
          placeholder="Enter your search query..."
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
        {loading ? 'Searching...' : 'Search'}
      </button>
    </form>
  );
}