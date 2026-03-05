'use client';

import { useState } from 'react';

export default function Home() {
  const [question, setQuestion] = useState('');
  const [chatResult, setChatResult] = useState<any>(null);
  const [prayerResult, setPrayerResult] = useState<any>(null);
  const [scenarioResult, setScenarioResult] = useState<any>(null);

  async function askChat() {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    setChatResult(await response.json());
  }

  async function loadPrayer() {
    const response = await fetch('http://localhost:8000/prayer?topic=焦虑');
    setPrayerResult(await response.json());
  }

  async function loadScenario() {
    const response = await fetch('http://localhost:8000/life-scenario?scenario=职场');
    setScenarioResult(await response.json());
  }

  return (
    <main style={{ maxWidth: 920, margin: '32px auto', fontFamily: 'sans-serif' }}>
      <h1>Bible AI Agent - Christian Use Cases</h1>

      <section>
        <h3>1) 圣经问答</h3>
        <textarea value={question} onChange={(e) => setQuestion(e.target.value)} style={{ width: '100%', minHeight: 80 }} />
        <button onClick={askChat} disabled={!question.trim()}>发送</button>
        {chatResult && <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(chatResult, null, 2)}</pre>}
      </section>

      <section style={{ marginTop: 24 }}>
        <h3>2) 祷告助手</h3>
        <button onClick={loadPrayer}>生成祷告引导（焦虑）</button>
        {prayerResult && <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(prayerResult, null, 2)}</pre>}
      </section>

      <section style={{ marginTop: 24 }}>
        <h3>3) 人生场景（基督徒语境）</h3>
        <button onClick={loadScenario}>职场场景建议</button>
        {scenarioResult && <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(scenarioResult, null, 2)}</pre>}
      </section>
    </main>
  );
}
