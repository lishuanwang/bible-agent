-- MySQL schema for Bible Agent
-- charset/collation
CREATE DATABASE IF NOT EXISTS bible_agent
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE bible_agent;

CREATE TABLE translations (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  code VARCHAR(32) NOT NULL UNIQUE,
  name VARCHAR(128) NOT NULL,
  language VARCHAR(32) NOT NULL,
  copyright_notice TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE verses (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  translation_id BIGINT NOT NULL,
  book VARCHAR(64) NOT NULL,
  chapter_num INT NOT NULL,
  verse_num INT NOT NULL,
  reference VARCHAR(64) NOT NULL,
  text TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_verses_translation FOREIGN KEY (translation_id) REFERENCES translations(id),
  UNIQUE KEY uniq_translation_bcv (translation_id, book, chapter_num, verse_num),
  KEY idx_reference (reference),
  FULLTEXT KEY ftx_verse_text (text)
);

CREATE TABLE verse_contexts (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  reference VARCHAR(64) NOT NULL UNIQUE,
  book VARCHAR(64) NOT NULL,
  author VARCHAR(128) NOT NULL,
  theme VARCHAR(128) NOT NULL,
  summary TEXT NOT NULL,
  nearby_refs VARCHAR(512) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE topics (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(128) NOT NULL UNIQUE,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE topic_verses (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  topic_id BIGINT NOT NULL,
  verse_id BIGINT NOT NULL,
  sort_order INT NOT NULL DEFAULT 0,
  CONSTRAINT fk_tv_topic FOREIGN KEY (topic_id) REFERENCES topics(id),
  CONSTRAINT fk_tv_verse FOREIGN KEY (verse_id) REFERENCES verses(id),
  UNIQUE KEY uniq_topic_verse (topic_id, verse_id),
  KEY idx_topic_sort (topic_id, sort_order)
);

-- optional: chat logs
CREATE TABLE chat_logs (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  question TEXT NOT NULL,
  answer LONGTEXT NOT NULL,
  theology_profile VARCHAR(64) NOT NULL,
  risk_flag TINYINT(1) NOT NULL DEFAULT 0,
  scope_flag TINYINT(1) NOT NULL DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
