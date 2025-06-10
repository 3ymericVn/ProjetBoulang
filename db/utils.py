import sqlite3

def init_db():
    with sqlite3.connect("db/clients.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                mail TEXT NOT NULL PRIMARY KEY,
                solde FLOAT DEFAULT 0.0 CHECK (solde >= 0)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                mail TEXT NOT NULL,
                date DATETIME NOT NULL DEFAULT (datetime('now','localtime')),
                montant FLOAT NOT NULL,
                operation TEXT NOT NULL,
                PRIMARY KEY (mail, date),
                FOREIGN KEY (mail) REFERENCES clients(mail)
            );
        """)
        conn.commit()

def add_client(nom: str, prenom: str, mail: str, solde: int = 0) -> bool:
    with sqlite3.connect("db/clients.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO clients (nom, prenom, mail, solde) VALUES (?, ?, ?, ?)",
                (nom, prenom, mail, solde)
            )
        except sqlite3.IntegrityError:
            print(f"Client with mail {mail} already exists.")
            return False
        conn.commit()
        return True

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

def operate_solde(mail: str, solde: float, operation: str) -> bool:
    solde = float(solde)
    with sqlite3.connect("db/clients.db") as conn:
        cursor = conn.cursor()
        op = "+" if operation == "add" else "-"
        try:
            cursor.execute(f"UPDATE clients SET solde = solde {op} ? WHERE mail = ?", (solde, mail))
            cursor.execute("INSERT INTO transactions (mail, montant, operation) VALUES (?, ?, ?)", (mail, solde, operation))
        except sqlite3.IntegrityError:
            print(f"Client with mail {mail} has a negative solde.")
            return False
        conn.commit()
        return True
