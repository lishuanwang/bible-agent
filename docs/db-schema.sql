-- PostgreSQL + pgvector schema draft

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE translations (
  id SERIAL PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  language TEXT NOT NULL,
  copyright_notice TEXT
);

CREATE TABLE verses (
  id BIGSERIAL PRIMARY KEY,
  translation_id INT NOT NULL REFERENCES translations(id),
  book TEXT NOT NULL,
  chapter INT NOT NULL,
  verse INT NOT NULL,
  reference TEXT NOT NULL,
  text TEXT NOT NULL,
  embedding vector(1536),
  UNIQUE (translation_id, book, chapter, verse)
);

CREATE INDEX idx_verses_reference ON verses(reference);
CREATE INDEX idx_verses_text_tsv ON verses USING GIN (to_tsvector('simple', text));
CREATE INDEX idx_verses_embedding ON verses USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE TABLE theology_profiles (
  id SERIAL PRIMARY KEY,
  key TEXT UNIQUE NOT NULL,
  display_name TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE chat_logs (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT now(),
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  theology_profile TEXT NOT NULL,
  risk_flag BOOLEAN DEFAULT FALSE
);
