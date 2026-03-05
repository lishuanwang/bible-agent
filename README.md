# bible-agent

全功能圣经 AI Agent 基础版（FastAPI + Next.js + PostgreSQL/pgvector 设计）。

## 已实现能力（MVP+）
- 经文查询：`/verse`
- 多译本对照：`/compare`
- 经文上下文：`/context`
- 关键词检索：`/search`
- 主题研经：`/topic`
- 灵修计划：`/devotional`
- 讲章/小组问题草案：`/sermon`
- 安全问答：`/chat`（高风险关键词转介）

## Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Frontend
```bash
cd frontend
npm install
npm run dev
```

## Test
```bash
cd backend
pytest
```
