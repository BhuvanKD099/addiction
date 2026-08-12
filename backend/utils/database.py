import sqlite3
import os
import re

try:
    from flask_mysqldb import MySQL as RealMySQL
except ImportError:
    RealMySQL = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_FILE = os.path.join(BASE_DIR, "database", "addictionsense.db")

class SQLiteCursorWrapper:
    def __init__(self, sqlite_conn):
        self.conn = sqlite_conn
        self.cursor = sqlite_conn.cursor()
        self.lastrowid = None

    def execute(self, query, params=None):
        sqlite_query = query.replace("%s", "?")
        sqlite_query = re.sub(r'AUTO_INCREMENT', 'AUTOINCREMENT', sqlite_query, flags=re.IGNORECASE)
        sqlite_query = re.sub(r'ENGINE\s*=\s*InnoDB', '', sqlite_query, flags=re.IGNORECASE)
        sqlite_query = re.sub(r'DEFAULT\s+CHARSET\s*=\s*\w+', '', sqlite_query, flags=re.IGNORECASE)
        sqlite_query = re.sub(r'NOW\(\)', "DATETIME('now')", sqlite_query, flags=re.IGNORECASE)
        sqlite_query = re.sub(r'CURRENT_TIMESTAMP\(\)', "DATETIME('now')", sqlite_query, flags=re.IGNORECASE)
        sqlite_query = re.sub(r'\bUSE\b\s+\w+;', '', sqlite_query, flags=re.IGNORECASE)
        sqlite_query = re.sub(r'\bCREATE\s+DATABASE\b.*?;', '', sqlite_query, flags=re.IGNORECASE)

        if params is None:
            params = ()
        if isinstance(params, list):
            params = tuple(params)

        res = self.cursor.execute(sqlite_query, params)
        self.lastrowid = self.cursor.lastrowid
        return res

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()

class SQLiteConnectionWrapper:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        is_new = not os.path.exists(self.db_path)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        if is_new:
            self._init_sqlite_db()

    def _init_sqlite_db(self):
        schema_path = os.path.join(os.path.dirname(self.db_path), "schema.sql")
        seed_path = os.path.join(os.path.dirname(self.db_path), "seed.sql")
        cursor = self._conn.cursor()

        if os.path.exists(schema_path):
            with open(schema_path, "r", encoding="utf-8") as f:
                sql_content = f.read()
            lines = [l for l in sql_content.splitlines() if not l.strip().startswith('--')]
            sql_clean = '\n'.join(lines)
            sql_clean = re.sub(r'INT\s+AUTO_INCREMENT\s+PRIMARY\s+KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT', sql_clean, flags=re.IGNORECASE)
            sql_clean = re.sub(r'ENGINE\s*=\s*InnoDB', '', sql_clean, flags=re.IGNORECASE)
            sql_clean = re.sub(r'DEFAULT\s+CHARSET\s*=\s*\w+', '', sql_clean, flags=re.IGNORECASE)
            sql_clean = re.sub(r'\bCREATE\s+DATABASE\b.*?;', '', sql_clean, flags=re.IGNORECASE)
            sql_clean = re.sub(r'\bUSE\b\s+.*?;', '', sql_clean, flags=re.IGNORECASE)
            sql_clean = re.sub(r'ENUM\(.*?\)', 'VARCHAR(50)', sql_clean, flags=re.IGNORECASE)

            statements = [s.strip() for s in sql_clean.split(";") if s.strip()]
            for stmt in statements:
                try:
                    cursor.execute(stmt)
                except Exception as e:
                    print("SQLite schema warning:", e)

        if os.path.exists(seed_path):
            with open(seed_path, "r", encoding="utf-8") as f:
                seed_content = f.read()
            seed_lines = [l for l in seed_content.splitlines() if not l.strip().startswith('--')]
            seed_clean = '\n'.join(seed_lines)
            seed_clean = re.sub(r'SET\s+FOREIGN_KEY_CHECKS\s*=\s*[01];', '', seed_clean, flags=re.IGNORECASE)
            seed_clean = re.sub(r'TRUNCATE\s+TABLE', 'DELETE FROM', seed_clean, flags=re.IGNORECASE)
            seed_clean = re.sub(r'\bUSE\b\s+.*?;', '', seed_clean, flags=re.IGNORECASE)

            statements = [s.strip() for s in seed_clean.split(";") if s.strip()]
            for stmt in statements:
                try:
                    cursor.execute(stmt)
                except Exception as e:
                    print("SQLite seed warning:", e)

        self._conn.commit()

    def cursor(self):
        return SQLiteCursorWrapper(self._conn)

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()

_sqlite_instance = None

def get_sqlite_conn():
    global _sqlite_instance
    if _sqlite_instance is None:
        _sqlite_instance = SQLiteConnectionWrapper()
    return _sqlite_instance

class SafeMySQL:
    def __init__(self, app=None):
        if RealMySQL:
            self._real_mysql = RealMySQL(app)
        else:
            self._real_mysql = None

    def init_app(self, app):
        if self._real_mysql:
            try:
                self._real_mysql.init_app(app)
            except Exception as e:
                print("Note: MySQL init skipped, using SQLite backend fallback.")

    @property
    def connection(self):
        if self._real_mysql:
            try:
                conn = self._real_mysql.connection
                if conn:
                    test_cur = conn.cursor()
                    test_cur.execute("SELECT 1")
                    test_cur.close()
                    return conn
            except Exception:
                pass
        return get_sqlite_conn()

mysql = SafeMySQL()