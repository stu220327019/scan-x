CREATE TABLE IF NOT EXISTS file (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  filename TEXT NOT NULL,
  filepath TEXT NOT NULL,
  path TEXT NOT NULL,
  sha1 TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  md5 TEXT NOT NULL,
  size INTEGER NOT NULL,
  type TEXT NOT NULL,
  created_at DATETIME NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_file_filpath_sha1 ON file(filepath, sha1);
CREATE UNIQUE INDEX IF NOT EXISTS ux_file_filpath_sha256 ON file(filepath, sha256);
CREATE UNIQUE INDEX IF NOT EXISTS ux_file_filpath_md5 ON file(filepath, md5);

CREATE TABLE IF NOT EXISTS file_scan_result (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  file_id INTEGER NOT NULL,
  analysis_stats TEXT NOT NULL,
  analysis_results TEXT NOT NULL,
  clean BOOLEAN NOT NULL,
  started_at DATETIME NOT NULL,
  finished_at DATETIME NOT NULL,
  created_at DATETIME NOT NULL,
  FOREIGN KEY (file_id) REFERENCES file(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS url (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  url TEXT NOT NULL UNIQUE,
  created_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS url_http_response (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  url_id INTEGER NOT NULL,
  status_code INT,
  content_length INT,
  content_sha256 TEXT,
  title TEXT,
  headers TEXT,
  created_at DATETIME NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_url_http_response_url_sha256 ON url_http_response(url_id, content_sha256);

CREATE TABLE IF NOT EXISTS url_scan_result (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  url_id INTEGER NOT NULL,
  url_http_response_id INTEGER NOT NULL,
  analysis_stats TEXT NOT NULL,
  analysis_results TEXT NOT NULL,
  clean BOOLEAN NOT NULL,
  started_at DATETIME NOT NULL,
  finished_at DATETIME NOT NULL,
  created_at DATETIME NOT NULL,
  FOREIGN KEY (url_id) REFERENCES url(id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (url_http_response_id) REFERENCES url_http_response(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS engine (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS virus (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS analysis (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  engine_id INTEGER NOT NULL,
  virus_id INTEGER,
  category TEXT /* CHECK( pType IN ('failure', 'harmless', 'malicious', 'suspicious', 'timeout', 'type-unsupported', 'undetected') ) */ NOT NULL,
  type TEXT /* CHECK( pType IN ('file', 'url') ) */ NOT NULL,
  file_scan_result_id INTEGER,
  url_scan_result_id INTEGER,
  FOREIGN KEY (engine_id) REFERENCES engine(id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (virus_id) REFERENCES virus(id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (file_scan_result_id) REFERENCES file_scan_result(id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (url_scan_result_id) REFERENCES url_scan_result(id) ON UPDATE CASCADE ON DELETE CASCADE
);
