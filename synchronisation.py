import pymysql
from pymongo import MongoClient

# Connexion à la base de données MySQL
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='InventaireDB'
)
cursor = conn.cursor(pymysql.cursors.DictCursor)

# Connexion à MongoDB
mongo_client = MongoClient("mongodb+srv://zackDB:2311@cluster0.uzwuxhn.mongodb.net/")
mongo_db = mongo_client.InventaireDB


def sync_fournisseurs():
    print("Synchronisation des Fournisseurs en cours...")
    cursor.execute("SELECT * FROM Fournisseurs")
    fournisseurs = cursor.fetchall()
    
    for fournisseur in fournisseurs:
        mongo_db.Fournisseurs.replace_one(
            {"id": fournisseur['id']}, fournisseur, upsert=True)
    print(f"{len(fournisseurs)} Fournisseurs synchronisés avec succès.")


def sync_produits():
    print("Synchronisation des Produits en cours...")
    cursor.execute("SELECT * FROM Produits")
    produits = cursor.fetchall()

    for produit in produits:
        mongo_db.Produits.replace_one(
            {"id": produit['id']}, produit, upsert=True)
    print(f"{len(produits)} Produits synchronisés avec succès.")


def sync_stock():
    print("Synchronisation du Stock en cours...")
    cursor.execute("SELECT * FROM Stock")
    stocks = cursor.fetchall()

    for stock_item in stocks:
        mongo_db.Stock.replace_one(
            {"produit_id": stock_item['produit_id']}, stock_item, upsert=True)
    print(f"{len(stocks)} éléments de Stock synchronisés avec succès.")


def sync_historique():
    print("Synchronisation de l'Historique en cours...")
    cursor.execute("SELECT * FROM Historique")
    historiques = cursor.fetchall()

    for historique in historiques:
        mongo_db.Historique.replace_one(
            {"id": historique['id']}, historique, upsert=True)
    print(f"{len(historiques)} entrées d'Historique synchronisées avec succès.")


def sync_clients():
    print("Synchronisation des Clients en cours...")
    cursor.execute("SELECT * FROM Clients")
    clients = cursor.fetchall()

    for client in clients:
        mongo_db.Clients.replace_one(
            {"id": client['id']}, client, upsert=True)
    print(f"{len(clients)} Clients synchronisés avec succès.")


def sync_commandes():
    print("Synchronisation des Commandes en cours...")
    cursor.execute("SELECT * FROM Commandes")
    commandes = cursor.fetchall()

    for commande in commandes:
        mongo_db.Commandes.replace_one(
            {"id": commande['id']}, commande, upsert=True)
    print(f"{len(commandes)} Commandes synchronisées avec succès.")


if __name__ == '__main__':
    try:
        sync_fournisseurs()
        sync_produits()
        sync_stock()
        sync_historique()
        sync_clients()
        sync_commandes()
        print("Synchronisation terminée avec succès!")
    except Exception as e:
        print(f"Erreur lors de la synchronisation: {e}")
    finally:
        # Fermez la connexion MySQL après la synchronisation
        cursor.close()
        conn.close()