import React from 'react';
import Markdown from 'react-markdown';

export default function MarkdownEditor({ markdown, onChange }) {
  return (
    <div style={{ display: 'flex', gap: 24 }}>
      <textarea
        style={{ width: '50%', minHeight: 400 }}
        value={markdown}
        onChange={e => onChange(e.target.value)}
      />
      <div style={{ width: '50%', minHeight: 400, border: '1px solid #ccc', padding: 12, background: '#fafbfc', overflow: 'auto' }}>
        <Markdown>{markdown}</Markdown>
      </div>
    </div>
  );
}
