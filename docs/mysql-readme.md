# MySQL 数据库设计与接入说明

本项目已改为**所有圣经与主题数据均从 MySQL 读取**，不再依赖内存字典。

## 1. 数据库结构
请执行 `docs/db-schema.sql` 初始化：

```bash
mysql -u root -p < docs/db-schema.sql
```

核心表：
- `translations`: 译本元数据（CUV/NIV 等）
- `verses`: 经文正文（按译本存储）
- `verse_contexts`: 经文上下文/背景信息
- `topics`: 主题（安慰/焦虑/祷告/职场等）
- `topic_verses`: 主题与经文多对多映射
- `chat_logs`（可选）: 问答审计日志

## 2. 环境变量
后端启动前需设置：

```bash
export MYSQL_HOST="127.0.0.1"
export MYSQL_PORT="3306"
export MYSQL_USER="root"
export MYSQL_PASSWORD="your_password"
export MYSQL_DATABASE="bible_agent"
```

## 3. 种子数据建议
至少准备以下数据：
1. `translations` 插入 CUV/NIV。
2. `verses` 插入基础经文（如 John 3:16、Romans 8:28、Psalm 23:1、Philippians 4:6、James 1:5）。
3. `topics` 插入：安慰、焦虑、祷告、智慧、婚姻、职场。
4. `topic_verses` 建立对应关系。
5. `verse_contexts` 插入常用经文背景。

## 4. 后端查询映射
- `/verse` -> `verses + translations`
- `/compare` -> `verses + translations`
- `/context` -> `verse_contexts`
- `/search` -> `verses`（LIKE/FULLTEXT 可进一步优化）
- `/topic` `/devotional` `/prayer` `/life-scenario` `/group-session` -> `topics + topic_verses + verses`

## 5. 生产建议
- 对 `verses(reference)`、`topic_verses(topic_id, sort_order)` 建索引（schema 已包含）。
- 长期可引入分词检索（Elastic/OpenSearch）提高中文检索效果。
- 建议把经文导入流程做成 ETL 脚本并做版权审计。
