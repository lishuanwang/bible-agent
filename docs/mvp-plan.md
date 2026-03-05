# Bible AI Agent MVP 周计划（FastAPI + Next.js + PostgreSQL/pgvector）

## 第 1 周：基础设施与数据
- 建立 PostgreSQL 数据库和 `verses`、`translations` 基础表。
- 导入单译本（建议先和合本）作为 MVP 数据。
- 实现 `/health`、`/verse` API。

## 第 2 周：检索与回答
- 实现关键词检索 `/search`。
- 引入 pgvector（可选）支持语义检索。
- 实现 `/chat`，回答需带证据经文。

## 第 3 周：安全与边界
- 增加高风险关键词检测与转介模板。
- 加入“不能替代专业人员”声明。
- 增加日志与问题追踪。

## 第 4 周：前端与联调
- 建立 Next.js 聊天页面。
- 显示回答、证据经文、风险提示。
- 完成端到端验证和部署文档。
