-- Création de la base de données
CREATE DATABASE Magasin;

-- Utilisation de la base de données
USE Magasin;

-- Table Produits
CREATE TABLE Produits (
    ID_Produit INT PRIMARY KEY AUTO_INCREMENT,
    Nom_Produit VARCHAR(255) NOT NULL,
    Description TEXT,
    Prix_Unitaire DECIMAL(10, 2) NOT NULL
);

-- Table Fournisseurs
CREATE TABLE Fournisseurs (
    ID_Fournisseur INT PRIMARY KEY AUTO_INCREMENT,
    Nom_Fournisseur VARCHAR(255) NOT NULL,
    Adresse TEXT NOT NULL,
    Téléphone VARCHAR(15)
);

-- Table Stock
CREATE TABLE Stock (
    ID_Stock INT PRIMARY KEY AUTO_INCREMENT,
    ID_Produit INT,
    Quantité INT NOT NULL,
    FOREIGN KEY (ID_Produit) REFERENCES Produits(ID_Produit)
);

-- Table Historique
CREATE TABLE Historique (
    ID_Historique INT PRIMARY KEY AUTO_INCREMENT,
    ID_Produit INT,
    Date DATE NOT NULL,
    Action ENUM('Achat', 'Vente') NOT NULL,
    Quantité INT NOT NULL,
    FOREIGN KEY (ID_Produit) REFERENCES Produits(ID_Produit)
);

-- Table Clients
CREATE TABLE Clients (
    ID_Client INT PRIMARY KEY AUTO_INCREMENT,
    Nom_Client VARCHAR(255) NOT NULL,
    Prénom_Client VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Adresse TEXT,
    Téléphone VARCHAR(15),
    Date_Inscription DATE DEFAULT CURRENT_DATE
);
