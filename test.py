import sqlite3
from db.utils import init_db, add_client, operate_solde, get_client_solde
import random
from datetime import datetime, timedelta
import string
import asyncio

from env import DB

CONNECTION = DB

def generate_random_name(min_length=4, max_length=8):
    """Génère un nom aléatoire avec une longueur entre min_length et max_length"""
    length = random.randint(min_length, max_length)
    # Première lettre en majuscule, reste en minuscules
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length)).capitalize()

def generate_random_email(nom, prenom):
    """Génère un email aléatoire basé sur le nom et prénom"""
    domains = ["gmail.com", "yahoo.fr", "hotmail.fr", "outlook.fr"]
    return f"{prenom.lower()}.{nom.lower()}@{random.choice(domains)}"

async def create_test_data(num_clients=20, transactions_per_client=5):
    """Crée des données de test avec des clients et des transactions"""
    # Initialiser la base de données
    await init_db()
    
    # Créer des clients
    clients = []
    for _ in range(num_clients):
        nom = generate_random_name(5, 10)
        prenom = generate_random_name(4, 8)
        email = generate_random_email(nom, prenom)
        solde_initial = random.randint(100, 500)
        
        if await add_client(nom, prenom, email, solde_initial):
            clients.append(email)
            #print(f"Client créé: {prenom} {nom} ({email})")
    
    # Créer des transactions pour chaque client
    operations = ["add", "remove"]
    for email in clients:
        for _ in range(transactions_per_client):
            operation = random.choice(operations)
            current_solde = await get_client_solde(email)
            
            if operation == "add":
                montant = round(random.uniform(5, 50), 2)
            else:  # remove
                max_remove = min(current_solde, 50)
                montant = round(random.uniform(5, max_remove), 2)
            
            if await operate_solde(email, montant, operation):
                pass

if __name__ == "__main__":
    print("Génération des données de test...")
    asyncio.run(create_test_data())
    print("Génération terminée!")
