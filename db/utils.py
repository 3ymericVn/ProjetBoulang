import asyncpg
import env

CONNECTION = env.DB_DEV

async def init_db():
    pool = await asyncpg.create_pool(CONNECTION)
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                mail TEXT NOT NULL PRIMARY KEY,
                solde FLOAT DEFAULT 0.0 CHECK (solde >= 0)
            );
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                mail TEXT NOT NULL,
                date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                montant FLOAT NOT NULL,
                operation TEXT NOT NULL,
                PRIMARY KEY (mail, date),
                FOREIGN KEY (mail) REFERENCES clients(mail)
            );
        """)
    await pool.close()

async def get_clients() -> list[asyncpg.Record]:
    pool = await asyncpg.create_pool(CONNECTION)
    async with pool.acquire() as conn:
        clients =await conn.fetch("SELECT * FROM clients")
    await pool.close()
    return clients

async def get_transactions() -> list[asyncpg.Record]:
    pool = await asyncpg.create_pool(CONNECTION)
    async with pool.acquire() as conn:
        transactions = await conn.fetch("""
            SELECT t.*, c.nom, c.prenom 
            FROM transactions t 
            JOIN clients c ON t.mail = c.mail
            ORDER BY t.date DESC
        """)
    await pool.close()
    return transactions

async def add_client(nom: str, prenom: str, mail: str, solde: float = 0) -> bool:
    pool = await asyncpg.create_pool(CONNECTION)
    async with pool.acquire() as conn:
        try:
            await conn.execute("INSERT INTO clients (nom, prenom, mail, solde) VALUES ($1, $2, $3, $4)", nom, prenom, mail, float(solde))
        except asyncpg.UniqueViolationError:
            return False
    await pool.close()
    return True

async def operate_solde(mail: str, solde: float, operation: str) -> bool:
    pool = await asyncpg.create_pool(CONNECTION)
    async with pool.acquire() as conn:
        try:
            op = "+" if operation == "add" else "-"
            await conn.execute(f"UPDATE clients SET solde = solde {op} $1 WHERE mail = $2", float(solde), mail)
            await conn.execute("INSERT INTO transactions (mail, montant, operation) VALUES ($1, $2, $3)", mail, float(solde), operation)
        except (asyncpg.ForeignKeyViolationError, asyncpg.exceptions.CheckViolationError):
            return False
    await pool.close()
    return True

async def delete_client(mail: str) -> bool:
    pool = await asyncpg.create_pool(CONNECTION)
    async with pool.acquire() as conn:
        try:
            await conn.execute("DELETE FROM clients WHERE mail = $1", mail)
        except asyncpg.ForeignKeyViolationError:
            return False
    await pool.close()
    return True

async def edit_client(mail: str, nom: str, prenom: str) -> bool:
    pool = await asyncpg.create_pool(CONNECTION)
    async with pool.acquire() as conn:
        try:
            await conn.execute("UPDATE clients SET nom = $1, prenom = $2 WHERE mail = $3", nom, prenom, mail)
        except asyncpg.UniqueViolationError:
            return False
    await pool.close()
    return True

async def get_client_solde(mail: str) -> float:
    pool = await asyncpg.create_pool(CONNECTION)
    async with pool.acquire() as conn:
        solde = await conn.fetchval("SELECT solde FROM clients WHERE mail = $1", mail)
        if solde is None:
            return 0.0
    await pool.close()
    return solde

async def get_transactions_by_mail(mail: str) -> list[asyncpg.Record]:
    pool = await asyncpg.create_pool(CONNECTION)
    async with pool.acquire() as conn:
        transactions = await conn.fetch("""
            SELECT t.*, c.nom, c.prenom 
            FROM transactions t 
            JOIN clients c ON t.mail = c.mail
            WHERE t.mail = $1
            ORDER BY t.date DESC
        """, mail)
    await pool.close()
    return transactions

async def search_client(query: str) -> list[asyncpg.Record]:
    pool = await asyncpg.create_pool(CONNECTION)
    async with pool.acquire() as conn:
        clients = await conn.fetch("SELECT * FROM clients WHERE nom LIKE $1 OR prenom LIKE $2 OR mail LIKE $3", f"%{query}%", f"%{query}%", f"%{query}%")
    await pool.close()
    return clients


# def init_db():
#     with sqlite3.connect(CONNECTION) as conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS clients (
#                 nom TEXT NOT NULL,
#                 prenom TEXT NOT NULL,
#                 mail TEXT NOT NULL PRIMARY KEY,
#                 solde FLOAT DEFAULT 0.0 CHECK (solde >= 0)
#             );
#         """)
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS transactions (
#                 mail TEXT NOT NULL,
#                 date DATETIME NOT NULL DEFAULT (datetime('now','localtime')),
#                 montant FLOAT NOT NULL,
#                 operation TEXT NOT NULL,
#                 PRIMARY KEY (mail, date),
#                 FOREIGN KEY (mail) REFERENCES clients(mail)
#             );
#         """)
#         conn.commit()

# def add_client(nom: str, prenom: str, mail: str, solde: int = 0) -> bool:
#     with sqlite3.connect("db/clients.db") as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         try:
#             cursor.execute(
#                 "INSERT INTO clients (nom, prenom, mail, solde) VALUES (?, ?, ?, ?)",
#                 (nom, prenom, mail, solde)
#             )
#         except sqlite3.IntegrityError:
#             print(f"Client with mail {mail} already exists.")
#             return False
#         conn.commit()
#         return True

# def get_clients() -> list[sqlite3.Row]:
#     with sqlite3.connect("db/clients.db") as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM clients")
#         return cursor.fetchall()

# def search_client(query: str) -> list[sqlite3.Row]:
#     with sqlite3.connect("db/clients.db") as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM clients WHERE nom LIKE ? OR prenom LIKE ? OR mail LIKE ?", (f"%{query}%", f"%{query}%", f"%{query}%"))
#         return cursor.fetchall()

# def operate_solde(mail: str, solde: float, operation: str) -> bool:
#     solde = float(solde)
#     with sqlite3.connect("db/clients.db") as conn:
#         cursor = conn.cursor()
#         op = "+" if operation == "add" else "-"
#         try:
#             cursor.execute(f"UPDATE clients SET solde = solde {op} ? WHERE mail = ?", (solde, mail))
#             cursor.execute("INSERT INTO transactions (mail, montant, operation) VALUES (?, ?, ?)", (mail, solde, operation))
#         except sqlite3.IntegrityError:
#             # print(f"Client with mail {mail} has a negative solde.")
#             return False
#         conn.commit()
#         return True

# def delete_client(mail: str) -> bool:
#     with sqlite3.connect("db/clients.db") as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute("DELETE FROM clients WHERE mail = ?", (mail,))
#         except sqlite3.IntegrityError:
#             print(f"Erreur lors de la suppression du client {mail}")
#             return False
#         conn.commit()
#         return True

# def edit_client(mail: str, nom: str, prenom: str) -> bool:
#     with sqlite3.connect("db/clients.db") as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute("UPDATE clients SET nom = ?, prenom = ?, mail = ? WHERE mail = ?", (nom, prenom, mail, mail))
#         except sqlite3.IntegrityError:
#             print(f"Erreur lors de la modification du client {mail}")
#             return False
#         conn.commit()
#         return True

# def get_client_solde(mail: str) -> float:
#     with sqlite3.connect("db/clients.db") as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute("SELECT solde FROM clients WHERE mail = ?", (mail,))
#         result = cursor.fetchone()
#         return result['solde'] if result else 0.0
    
# def get_transactions() -> list[sqlite3.Row]:
#     with sqlite3.connect("db/clients.db") as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT t.*, c.nom, c.prenom 
#             FROM transactions t 
#             JOIN clients c ON t.mail = c.mail
#             ORDER BY t.date DESC
#         """)
#         return cursor.fetchall()

# def get_transactions_by_mail(mail: str) -> list[sqlite3.Row]:
#     with sqlite3.connect("db/clients.db") as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT t.*, c.nom, c.prenom 
#             FROM transactions t 
#             JOIN clients c ON t.mail = c.mail
#             WHERE t.mail = ?
#             ORDER BY t.date DESC
#         """, (mail,))
#         return cursor.fetchall()
