import sqlite3

def init_db():
    with sqlite3.connect("db/clients.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                mail TEXT NOT NULL PRIMARY KEY
            )
        """)
        conn.commit()

def add_client(nom: str, prenom: str, mail: str):
    with sqlite3.connect("db/clients.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clients (nom, prenom, mail) VALUES (?, ?, ?)", (nom, prenom, mail))
        conn.commit()

def get_clients() -> list[sqlite3.Row]:
    with sqlite3.connect("db/clients.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        return cursor.fetchall()

def search_client(query: str) -> list[sqlite3.Row]:
    with sqlite3.connect("db/clients.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE nom LIKE ? OR prenom LIKE ? OR mail LIKE ?", (f"%{query}%", f"%{query}%", f"%{query}%"))
        return cursor.fetchall()