DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  github_id TEXT,
  google_id TEXT,
  facebook_id TEXT,
  name TEXT NOT NULL DEFAULT '',
  avatar TEXT NOT NULL DEFAULT '',
  last_login TIMESTAMPTZ
);
CREATE UNIQUE INDEX ON users (github_id);
CREATE UNIQUE INDEX ON users (google_id);
CREATE UNIQUE INDEX ON users (facebook_id);


DROP TABLE IF EXISTS posts CASCADE;
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  author_id INTEGER NOT NULL,
  created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  message TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES users (id)
);
