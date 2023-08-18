CREATE TABLE Fournisseurs (
    fournisseurID INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    adresse VARCHAR(255),
    telephone VARCHAR(20)
);

CREATE TABLE Produits (
    produitID INT AUTO_INCREMENT PRIMARY KEY,
    fournisseurID INT,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    prix DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (fournisseurID) REFERENCES Fournisseurs(fournisseurID)
);

CREATE TABLE Stock (
    stockID INT AUTO_INCREMENT PRIMARY KEY,
    produitID INT,
    quantite INT NOT NULL,
    FOREIGN KEY (produitID) REFERENCES Produits(produitID)
);

CREATE TABLE Client (
    clientID INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    adresse VARCHAR(255),
    telephone VARCHAR(20)
);

CREATE TABLE Commande (
    commandeID INT AUTO_INCREMENT PRIMARY KEY,
    clientID INT,
    date DATE NOT NULL,
    FOREIGN KEY (clientID) REFERENCES Client(clientID)
);

CREATE TABLE Historique (
    historiqueID INT AUTO_INCREMENT PRIMARY KEY,
    produitID INT,
    date DATE NOT NULL,
    action VARCHAR(50) NOT NULL,
    quantite INT NOT NULL,
    FOREIGN KEY (produitID) REFERENCES Produits(produitID)
);

CREATE TABLE DetailsCommande (
    detailsCommandeID INT AUTO_INCREMENT PRIMARY KEY,
    commandeID INT,
    produitID INT,
    quantite INT NOT NULL,
    FOREIGN KEY (commandeID) REFERENCES Commande(commandeID),
    FOREIGN KEY (produitID) REFERENCES Produits(produitID)
);
