import config

# Définir des schémas pour les tables/collections
SCHEMAS = {
    "Produits": {
        "fields": ["Nom_Produit", "Description", "Prix_Unitaire"],
        "primary_key": "ID_Produit",
        "mysql_insert": "INSERT INTO Produits (Nom_Produit, Description, Prix_Unitaire) VALUES (%s, %s, %s)",
        "mysql_update": "UPDATE Produits SET Nom_Produit = %s, Description = %s, Prix_Unitaire = %s WHERE ID_Produit = %s",
        "mysql_delete": "DELETE FROM Produits WHERE ID_Produit = %s"
    },
    "Fournisseurs": {
        "fields": ["Nom_Fournisseur", "Adresse", "Téléphone"],
        "primary_key": "ID_Fournisseur",
        "mysql_insert": "INSERT INTO Fournisseurs (Nom_Fournisseur, Adresse, Téléphone) VALUES (%s, %s, %s)",
        "mysql_update": "UPDATE Fournisseurs SET Nom_Fournisseur = %s, Adresse = %s, Téléphone = %s WHERE ID_Fournisseur = %s",
        "mysql_delete": "DELETE FROM Fournisseurs WHERE ID_Fournisseur = %s"
    },
    "Stock": {
        "fields": ["ID_Produit", "Quantité"],
        "primary_key": "ID_Stock",
        "mysql_insert": "INSERT INTO Stock (ID_Produit, Quantité) VALUES (%s, %s)",
        "mysql_update": "UPDATE Stock SET ID_Produit = %s, Quantité = %s WHERE ID_Stock = %s",
        "mysql_delete": "DELETE FROM Stock WHERE ID_Stock = %s"
    },
    "Historique": {
        "fields": ["ID_Produit", "Date", "Action", "Quantité"],
        "primary_key": "ID_Historique",
        "mysql_insert": "INSERT INTO Historique (ID_Produit, Date, Action, Quantité) VALUES (%s, %s, %s, %s)",
        "mysql_update": "UPDATE Historique SET ID_Produit = %s, Date = %s, Action = %s, Quantité = %s WHERE ID_Historique = %s",
        "mysql_delete": "DELETE FROM Historique WHERE ID_Historique = %s"
    },
    "Clients": {
        "fields": ["Nom_Client", "Prénom_Client", "Email", "Adresse", "Téléphone", "Date_Inscription"],
        "primary_key": "ID_Client",
        "mysql_insert": "INSERT INTO Clients (Nom_Client, Prénom_Client, Email, Adresse, Téléphone, Date_Inscription) VALUES (%s, %s, %s, %s, %s, %s)",
        "mysql_update": "UPDATE Clients SET Nom_Client = %s, Prénom_Client = %s, Email = %s, Adresse = %s, Téléphone = %s, Date_Inscription = %s WHERE ID_Client = %s",
        "mysql_delete": "DELETE FROM Clients WHERE ID_Client = %s"
    }
}

table_to_primary_key = {
    'Produits': 'ID_Produit',
    'Fournisseurs': 'ID_Fournisseur',
    'Stock': 'ID_Stock',
    'Historique': 'ID_Historique',
    'Clients': 'ID_Client'
}

configs = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "database": "Magasin",
    "raise_on_warnings": True
}