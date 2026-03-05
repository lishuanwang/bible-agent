# bible-agent

圣经类 AI Agent MVP（FastAPI + Next.js + PostgreSQL/pgvector 设计）。

## 目录
- `backend/`: FastAPI API（经文检索、问答、安全提示）
- `frontend/`: Next.js 聊天界面
- `docs/`: MVP 周计划、数据库草案、Prompt 与安全策略

## Backend 快速启动
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Frontend 快速启动
```bash
cd frontend
npm install
npm run dev
```

默认前端会请求 `http://localhost:8000/chat`。

## 测试
```bash
cd backend
pytest
```
