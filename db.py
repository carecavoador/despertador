import pathlib
import sqlite3
from datetime import datetime

from alarm import Alarm

DB_TIMERS = pathlib.Path("alarms.db")


class Database:
    """Database controller."""

    def __init__(self, db=DB_TIMERS) -> None:
        self._db = pathlib.Path(db)
        self._query(
            """CREATE TABLE IF NOT EXISTS tb_alarms (
                id INTEGER NOT NULL PRIMARY KEY,
                description TEXT,
                next_alarm TEXT);"""
        )

    def add_alarm(
        self,
        description: str,
        next_alarm: datetime
    ) -> None:
        """Adds a new alarm."""
        with sqlite3.connect(self._db) as conn:
            c = conn.cursor()
            c.execute(
                """INSERT INTO tb_alarms (
                    description,
                    next_alarm
                    ) VALUES (?, ?);""",
                [description, next_alarm],
            )
            return c.lastrowid

    def remove_alarm(self, key: int) -> None:
        """Remove a alarm by the primary key."""
        with sqlite3.connect(self._db) as conn:
            c = conn.cursor()
            c.execute("""DELETE FROM tb_alarms WHERE id=(?);""", (key,))

    def ring_alarm(self, key: int, next_alarm: datetime) -> None:
        """Remove a alarm by the primary key."""
        with sqlite3.connect(self._db) as conn:
            c = conn.cursor()
            c.execute(
                """UPDATE tb_alarms SET next_alarm = (?) WHERE id=(?);""",
                (next_alarm, key),
            )

    def _query(self, query: str) -> None:
        """DEBUG ONLY, directly execute queries."""
        with sqlite3.connect(self._db) as conn:
            c = conn.cursor()
            return c.execute(query)

    def list_alarms(self) -> list[Alarm]:
        """List of all alarms on the database."""
        with sqlite3.connect(self._db) as conn:
            c = conn.cursor()
            alarms = c.execute("SELECT * FROM tb_alarms;").fetchall()
            return [Alarm(t[0], t[1], datetime.fromisoformat(t[2])) for t in alarms]
