import { useState } from 'react';
import Head from 'next/head';
import SearchForm from '../components/SearchForm';
import ResultsList from '../components/ResultsList';
import axios from 'axios';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000';

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

  const handleSearch = async ({ url, query }) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      console.log('Sending request:', { url, query });
      const response = await axios.post(`${BACKEND_URL}/api/search`, {
        url,
        query
      });

      console.log('Received response:', response.data);
      setResults(response.data);
    } catch (err) {
      console.error('Search error:', err);
      setError(
        err.response?.data?.error || 
        err.message || 
        'An error occurred while searching'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Website Content Search</title>
        <meta name="description" content="Search through website content with precision" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="container">
        <header className="header">
          <h1>Website Content Search</h1>
          <p>Search through website content with precision</p>
        </header>

        <SearchForm onSearch={handleSearch} loading={loading} />

        {error && (
          <div className="error">
            <strong>Error:</strong> {error}
          </div>
        )}

        {results && (
          <ResultsList
            results={results.results}
            url={results.url}
            query={results.query}
            totalChunks={results.total_chunks}
          />
        )}
      </div>
    </>
  );
}