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
- 安全问答：`/chat`（高风险转介 + 语境边界提示 + 大模型调用）

## 配置大模型（必需）
`/chat` 已改为真实调用 OpenAI 兼容接口，请先设置：

```bash
export OPENAI_API_KEY="your_api_key"
export OPENAI_MODEL="gpt-4o-mini"
# 可选：自定义兼容网关
export OPENAI_BASE_URL="https://api.openai.com/v1"
```

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
