# Bible AI Agent 全功能路线图（当前仓库已落地基础实现）

## 已落地接口
- `/verse` 经文查询
- `/compare` 多译本对照
- `/context` 上下文信息
- `/search` 检索
- `/topic` 主题研经
- `/devotional` 灵修计划
- `/sermon` 讲章与小组问题草案
- `/chat` 安全问答

## 下一步生产化
1. 用 PostgreSQL + pgvector 替换内存数据。
2. 接入真实 LLM（函数调用/工具调用）。
3. 增加审计日志、用户体系、教会组织空间。
4. 引入评测集（引用准确率/幻觉率/安全命中率）。
