'use client';

import { useState } from 'react';

type SearchItem = {
  reference: string;
  text: string;
  score: number;
};

type ChatResponse = {
  answer: string;
  evidence: SearchItem[];
  safety_notice?: string | null;
};

export default function Home() {
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState(false);

  async function ask() {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });
      const data: ChatResponse = await response.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ maxWidth: 820, margin: '40px auto', fontFamily: 'sans-serif' }}>
      <h1>Bible AI Agent (MVP)</h1>
      <p>输入问题，系统会先检索经文，再生成结构化回答。</p>
      <textarea
        style={{ width: '100%', minHeight: 110 }}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="例如：苦难中的安慰经文有哪些？"
      />
      <button onClick={ask} disabled={loading || !question.trim()}>
        {loading ? '处理中...' : '发送'}
      </button>

      {result && (
        <section style={{ marginTop: 24 }}>
          {result.safety_notice && (
            <p style={{ color: '#b91c1c', fontWeight: 600 }}>{result.safety_notice}</p>
          )}
          <h3>回答</h3>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{result.answer}</pre>
          <h3>证据经文</h3>
          <ul>
            {result.evidence.map((item) => (
              <li key={item.reference}>
                <strong>{item.reference}</strong>：{item.text}
              </li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
}
