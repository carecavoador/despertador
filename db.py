import pathlib
import sqlite3

# DB_TIMERS = pathlib.Path().home().joinpath(".config/Despertador/alarmes.db")
DB_TIMERS = pathlib.Path("alarmes.db")


class Banco:
    """Controller para acessar e manipular o banco de dados."""
    def __init__(self, db: pathlib.Path=DB_TIMERS) -> None:
        self._db = pathlib.Path(db)
        self._query("""CREATE TABLE IF NOT EXISTS alarmes (id INTEGER NOT NULL PRIMARY KEY, descricao TEXT, hora INTEGER, minutos INTEGER);""")

    def add_alarme(self, descricao: str, hora: int, minutos: int) -> None:
        """Adiciona um novo lembrete."""
        with sqlite3.connect(self._db) as con:
            con.execute(
                "INSERT INTO alarmes (descricao, hora, minutos) VALUES (?, ?, ?);",
                [descricao, hora, minutos]
            )
            return con.cursor().lastrowid

    def remove_alarme(self, key: int) -> None:
        """Remove um lembrete pela id (primary key)."""
        with sqlite3.connect(self._db) as con:
            con.execute("DELETE FROM alarmes WHERE id=(?);", (key,))

    def _query(self, query: str) -> None:
        """APENAS PARA DEBUG. Executa querys direto no banco."""
        with sqlite3.connect(self._db) as con:
            return con.execute(query)

    @property
    def alarmes(self) -> list[tuple]:
        """Retorna uma lista com todos os alarmes."""
        with sqlite3.connect(self._db) as con:
            return con.execute("SELECT * FROM alarmes;").fetchall()
