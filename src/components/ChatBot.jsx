import React, { useState } from 'react';

export default function ChatBot() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [latency, setLatency] = useState(0);
  const [sessionId] = useState(() => {
    const stored = localStorage.getItem('session_id');
    if (stored) return stored;
    const newId = crypto.randomUUID();
    localStorage.setItem('session_id', newId);
    return newId;
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, session_id: sessionId })
      });

      const data = await response.json();
      setAnswer(data.answer);
      setSources(data.sources || []);
      setLatency(data.latency_ms || 0);
      setQuery('');
    } catch (error) {
      setAnswer('Chat service temporarily unavailable. Please try again.');
      setSources([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbot-container" style={{ display: isOpen ? 'block' : 'none' }}>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about the textbook..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Send'}
        </button>
      </form>
      {answer && (
        <div className="answer">
          <p>{answer}</p>
          {latency > 0 && <small>Answered in {latency}ms</small>}
          {sources.length > 0 && (
            <div className="sources">
              <h4>Sources</h4>
              {sources.map((src, i) => (
                <div key={i} className="source">
                  <strong>{src.chapter_title} - {src.section_title}</strong>
                  <p>{src.excerpt}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
