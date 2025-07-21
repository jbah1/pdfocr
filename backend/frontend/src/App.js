import React, { useState } from 'react';
import MarkdownEditor from './components/MarkdownEditor';
import './App.css';

function App() {
  const [markdown, setMarkdown] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = async (e) => {
    setError('');
    const file = e.target.files[0];
    if (!file) return;
    if (!file.name.endsWith('.pdf')) {
      setError('Only PDF files are supported.');
      return;
    }
    if (file.size > 50 * 1024 * 1024) {
      setError('File too large (max 50MB).');
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch('http://192.168.50.44:52560/upload', {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error('Failed to process PDF');
      const data = await res.json();
      setMarkdown(data.markdown);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App" style={{ maxWidth: 900, margin: '40px auto', padding: 24 }}>
      <h1>PDF Menu OCR to Markdown</h1>
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      {loading && <p>Processing PDF, please wait...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <MarkdownEditor markdown={markdown} onChange={setMarkdown} />
    </div>
  );
}

export default App;
