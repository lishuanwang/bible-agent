'use client';

import { useState } from 'react';

type SearchItem = { reference: string; text: string; score: number };

type ChatResponse = {
  answer: string;
  evidence: SearchItem[];
  safety_notice?: string | null;
};

export default function Home() {
  const [question, setQuestion] = useState('');
  const [chatResult, setChatResult] = useState<ChatResponse | null>(null);
  const [topicResult, setTopicResult] = useState<any>(null);
  const [devotionalResult, setDevotionalResult] = useState<any>(null);

  async function askChat() {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    setChatResult(await response.json());
  }

  async function loadTopic() {
    const response = await fetch('http://localhost:8000/topic?topic=安慰');
    setTopicResult(await response.json());
  }

  async function loadDevotional() {
    const response = await fetch('http://localhost:8000/devotional?theme=安慰&days=5');
    setDevotionalResult(await response.json());
  }

  return (
    <main style={{ maxWidth: 900, margin: '32px auto', fontFamily: 'sans-serif' }}>
      <h1>Bible AI Agent - Full Feature MVP</h1>

      <section>
        <h3>1) 问答（证据驱动）</h3>
        <textarea
          style={{ width: '100%', minHeight: 90 }}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="例如：在焦虑里该怎么祷告？"
        />
        <button onClick={askChat} disabled={!question.trim()}>发送问题</button>
        {chatResult && (
          <div>
            {chatResult.safety_notice && <p style={{ color: '#b91c1c' }}>{chatResult.safety_notice}</p>}
            <pre style={{ whiteSpace: 'pre-wrap' }}>{chatResult.answer}</pre>
          </div>
        )}
      </section>

      <section style={{ marginTop: 24 }}>
        <h3>2) 主题研经</h3>
        <button onClick={loadTopic}>加载“安慰”主题</button>
        {topicResult && <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(topicResult, null, 2)}</pre>}
      </section>

      <section style={{ marginTop: 24 }}>
        <h3>3) 灵修计划</h3>
        <button onClick={loadDevotional}>生成 5 天计划</button>
        {devotionalResult && <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(devotionalResult, null, 2)}</pre>}
      </section>
    </main>
  );
}
