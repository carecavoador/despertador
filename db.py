import pathlib
import sqlite3


DB_TIMERS = pathlib.Path("alarms.db")


class Database:
    """Database controller."""

    def __init__(self, db=DB_TIMERS) -> None:
        self._db = pathlib.Path(db)
        self._query(
            """CREATE TABLE IF NOT EXISTS tb_alarms (id INTEGER NOT NULL PRIMARY KEY, description TEXT, hour INTEGER, minutes INTEGER);"""
        )

    def add_alarm(self, description: str, hour: int, minutes: int) -> None:
        """Adds a new alarm."""
        with sqlite3.connect(self._db) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO tb_alarms (description, hour, minutes) VALUES (?, ?, ?);",
                [description, hour, minutes],
            )
            return c.lastrowid

    def remove_alarme(self, key: int) -> None:
        """Remove a alarm by the primary key."""
        with sqlite3.connect(self._db) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM tb_alarms WHERE id=(?);", (key,))

    def _query(self, query: str) -> None:
        """DEBUG ONLY, directly execute queries."""
        with sqlite3.connect(self._db) as conn:
            c = conn.cursor()
            return c.execute(query)

    @property
    def alarms(self) -> list[tuple]:
        """List of all alarms on the database."""
        with sqlite3.connect(self._db) as conn:
            c = conn.cursor()
            return c.execute("SELECT * FROM tb_alarms;").fetchall()
