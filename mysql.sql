-- Créer la base de données
CREATE DATABASE InventaireDB;

-- Utilisez cette base de données pour les opérations suivantes
USE InventaireDB;

-- Table des Fournisseurs
CREATE TABLE Fournisseurs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255) NOT NULL,
    contact VARCHAR(255),
    adresse TEXT
);

-- Table des Produits
CREATE TABLE Produits (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    prix DECIMAL(10,2) NOT NULL,
    fournisseur_id INT,
    FOREIGN KEY (fournisseur_id) REFERENCES Fournisseurs(id)
);

-- Table des Stocks
CREATE TABLE Stock (
    produit_id INT PRIMARY KEY,
    quantite INT DEFAULT 0,
    FOREIGN KEY (produit_id) REFERENCES Produits(id)
);

-- Table de l'Historique des Stocks
CREATE TABLE Historique (
    id INT PRIMARY KEY AUTO_INCREMENT,
    produit_id INT,
    quantite_change INT NOT NULL,
    date_change DATE NOT NULL,
    FOREIGN KEY (produit_id) REFERENCES Produits(id)
);

-- Table des Clients
CREATE TABLE Clients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255) NOT NULL,
    adresse TEXT,
    contact VARCHAR(255)
);

-- Table des Commandes
CREATE TABLE Commandes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    client_id INT,
    date_commande DATE NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Clients(id)
);

-- Table des Détails des Commandes
CREATE TABLE DetailsCommande (
    commande_id INT,
    produit_id INT,
    quantite INT NOT NULL,
    PRIMARY KEY (commande_id, produit_id),
    FOREIGN KEY (commande_id) REFERENCES Commandes(id),
    FOREIGN KEY (produit_id) REFERENCES Produits(id)
);
