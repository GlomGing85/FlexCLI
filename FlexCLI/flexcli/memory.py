from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class MemoryStore:
    def __init__(self, db_path: str):
        self.db_path = str(Path(db_path).expanduser())
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    tags TEXT DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def save_message(self, role: str, content: str) -> None:
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO messages(role, content) VALUES (?, ?)",
                (role, content),
            )
            conn.commit()

    def recent_messages(self, limit: int = 12) -> list[dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT role, content, created_at FROM messages ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        items = [dict(r) for r in rows]
        items.reverse()
        return items

    def clear_messages(self) -> None:
        with self._conn() as conn:
            conn.execute("DELETE FROM messages")
            conn.commit()

    def add_memory(self, text: str, tags: str = "") -> int:
        with self._conn() as conn:
            cur = conn.execute(
                "INSERT INTO memories(text, tags) VALUES (?, ?)",
                (text, tags),
            )
            conn.commit()
            return int(cur.lastrowid)

    def recent_memories(self, limit: int = 10) -> list[dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id, text, tags, created_at FROM memories ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]

    def search_memories(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        like = f"%{query}%"
        with self._conn() as conn:
            rows = conn.execute(
                """
                SELECT id, text, tags, created_at
                FROM memories
                WHERE text LIKE ? OR tags LIKE ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (like, like, limit),
            ).fetchall()
        return [dict(r) for r in rows]
