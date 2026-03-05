# bible-agent

面向圣经/基督教语境的 AI Agent（FastAPI + Next.js）。

## 功能（当前实现）
- 圣经检索：`/verse`、`/search`
- 多译本：`/compare`
- 上下文：`/context`
- 主题研经：`/topic`
- 灵修计划：`/devotional`
- 讲章大纲：`/sermon`
- 祷告助手：`/prayer`
- 门训计划：`/discipleship`
- 人生场景建议：`/life-scenario`
- 小组聚会模板：`/group-session`
- 安全问答：`/chat`（高风险转介 + 语境边界提示）

## 启动
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

```bash
cd frontend
npm install
npm run dev
```
