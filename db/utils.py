import pg8000
import asyncio
import env
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

CONNECTION = env.DB_DEV
_executor = ThreadPoolExecutor(max_workers=4)
_pool = []

def get_connection():
    # Parse connection string
    # postgresql://user:pass@host:port/dbname
    parts = CONNECTION.replace("postgresql://", "").split("@")
    user_pass = parts[0].split(":")
    host_db = parts[1].split("/")
    host_port = host_db[0].split(":")
    
    return pg8000.Connection(
        user=user_pass[0],
        password=user_pass[1],
        host=host_port[0],
        port=int(host_port[1]) if len(host_port) > 1 else 5432,
        database=host_db[1].split("?")[0]
    )

async def get_db_connection():
    """Get a connection from pool or create new one"""
    if _pool:
        return _pool.pop()
    return get_connection()

async def release_connection(conn):
    """Release connection back to pool"""
    if len(_pool) < 4:  # Max pool size
        _pool.append(conn)
    else:
        conn.close()

async def execute_query(query: str, params: tuple = None):
    """Execute a query asynchronously"""
    def _execute():
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                if query.strip().upper().startswith('SELECT'):
                    columns = [desc[0] for desc in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
                else:
                    conn.commit()
                    return True
        finally:
            conn.close()
    
    return await asyncio.get_event_loop().run_in_executor(_executor, _execute)

async def execute_transaction(queries: list):
    """Execute multiple queries in a transaction"""
    def _execute_transaction():
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                for query, params in queries:
                    cursor.execute(query, params or ())
                conn.commit()
                return True
        except Exception:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    return await asyncio.get_event_loop().run_in_executor(_executor, _execute_transaction)

async def init_db():
    await execute_query("""
        CREATE TABLE IF NOT EXISTS clients (
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            mail TEXT NOT NULL PRIMARY KEY,
            solde FLOAT DEFAULT 0.0 CHECK (solde >= 0)
        );
    """)
    await execute_query("""
        CREATE TABLE IF NOT EXISTS transactions (
            mail TEXT NOT NULL,
            date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            montant FLOAT NOT NULL,
            operation TEXT NOT NULL,
            PRIMARY KEY (mail, date),
            FOREIGN KEY (mail) REFERENCES clients(mail)
        );
    """)

async def get_clients():
    return await execute_query("SELECT * FROM clients")

async def get_transactions():
    return await execute_query("""
        SELECT t.*, c.nom, c.prenom 
        FROM transactions t 
        JOIN clients c ON t.mail = c.mail
        ORDER BY t.date DESC
    """)

async def add_client(nom: str, prenom: str, mail: str, solde: float = 0) -> bool:
    try:
        await execute_query(
            "INSERT INTO clients (nom, prenom, mail, solde) VALUES (%s, %s, %s, %s)",
            (nom, prenom, mail, float(solde))
        )
        return True
    except Exception:
        return False

async def operate_solde(mail: str, solde: float, operation: str) -> bool:
    op = "+" if operation == "add" else "-"
    queries = [
        (f"UPDATE clients SET solde = solde {op} %s WHERE mail = %s", (float(solde), mail)),
        ("INSERT INTO transactions (mail, montant, operation) VALUES (%s, %s, %s)", 
         (mail, float(solde), operation))
    ]
    return await execute_transaction(queries)

async def delete_client(mail: str) -> bool:
    try:
        await execute_query("DELETE FROM clients WHERE mail = %s", (mail,))
        return True
    except Exception:
        return False

async def edit_client(mail: str, nom: str, prenom: str) -> bool:
    try:
        await execute_query(
            "UPDATE clients SET nom = %s, prenom = %s WHERE mail = %s",
            (nom, prenom, mail)
        )
        return True
    except Exception:
        return False

async def get_client_solde(mail: str) -> float:
    result = await execute_query("SELECT solde FROM clients WHERE mail = %s", (mail,))
    return result[0]['solde'] if result else 0.0

async def get_transactions_by_mail(mail: str):
    return await execute_query("""
        SELECT t.*, c.nom, c.prenom 
        FROM transactions t 
        JOIN clients c ON t.mail = c.mail
        WHERE t.mail = %s
        ORDER BY t.date DESC
    """, (mail,))

async def search_client(query: str):
    return await execute_query(
        "SELECT * FROM clients WHERE nom LIKE %s OR prenom LIKE %s OR mail LIKE %s",
        (f"%{query}%", f"%{query}%", f"%{query}%")
    )

async def close_pool():
    """Close all connections in pool"""
    for conn in _pool:
        conn.close()
    _pool.clear()
    _executor.shutdown(wait=True)
