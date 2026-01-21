import { useState } from 'react';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!question.trim()) {
      alert('Please enter a question');
      return;
    }

    setLoading(true);
    setAnswer('');
    setSources([]);

    try {
      const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      setAnswer(data.answer);
      setSources(data.sources);
    } catch (error) {
      setAnswer('Error: Could not connect to backend. Make sure the server is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Cybersecurity Knowledge Assistant</h1>

      <div style={{ marginTop: '20px' }}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a cybersecurity question..."
          style={{
            width: '100%',
            padding: '10px',
            fontSize: '16px',
            marginBottom: '10px'
          }}
          onKeyPress={(e) => {
            if (e.key === 'Enter') handleSubmit();
          }}
        />

        <button
          onClick={handleSubmit}
          disabled={loading}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Loading...' : 'Submit'}
        </button>
      </div>

      {answer && (
        <div style={{ marginTop: '30px' }}>
          <h2>Answer:</h2>
          <p style={{
            padding: '15px',
            backgroundColor: '#f0f0f0',
            border: '1px solid #ccc'
          }}>
            {answer}
          </p>
        </div>
      )}

      {sources.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <h3>Sources:</h3>
          <ul>
            {sources.map((source, index) => (
              <li key={index}>{source}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
