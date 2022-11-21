import sqlite3


class TodoDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("quartodo.db", isolation_level=None)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS Todo
            (
                pk           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT              NOT NULL,
                is_completed INTEGER DEFAULT 0 NOT NULL,
                created      TEXT    DEFAULT current_timestamp 
            );
            """
        )

    def create(self, name):
        self.connection.execute("""INSERT INTO Todo (name) VALUES (?);""", [name])

    def update(self, pk, name):
        self.connection.execute("""UPDATE Todo SET name = ? WHERE pk = ?;""", [name, pk])

    def toggle(self, pk, completed):
        self.connection.execute("""UPDATE Todo SET is_completed = ? WHERE pk = ?;""", [completed, pk])

    def delete(self, pk):
        self.connection.execute("""DELETE FROM Todo WHERE pk = ?;""", [pk])

    def get(self, pk):
        result = self.connection.execute("""SELECT * FROM Todo WHERE pk = ?;""", [pk]).fetchone()
        return dict(result)

    def list(self):
        result = self.connection.execute("""SELECT * FROM Todo ORDER BY created DESC;""").fetchall()
        return list(map(dict, result))


db = TodoDatabase()
