import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(["tital","butg"]);
  // const [logined

  const handleChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.get(`http://10.145.243.15:8080/search?q=${query}`);
      console.log(response.data.results)
      setResults(response.data.results);
      localStorage.setItem("first_movie", response.data.results[0])
    } catch (error) {
      console.error('Error fetching data:', error);
      
    }
  };

  return (
    <div>
      <h1>Search App</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={handleChange}
          placeholder="Enter search query"
        />
        <button type="submit">Search</button>
      </form>
      <ul>
        {results.map((result, index) => (
          <li key={index}>{result}</li>
          // Assuming each result has a 'name' property, replace it with appropriate field
        ))}
      </ul>
    </div>
  );
}

export default App;
