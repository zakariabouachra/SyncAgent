const { pool } = require('../config/database');
const Produit = require('../models/Produits');

// GET - Récupérer tous les produits
exports.getAllProduits = async (req, res) => {
    try {
        const [produitsFromMySQL] = await pool.query('SELECT * FROM Produits');
        const produitsFromMongo = await Produit.find();

        res.status(200).json({
            mysql: produitsFromMySQL,
            mongodb: produitsFromMongo
        });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// GET - Récupérer un produit par ID
exports.getProduitById = async (req, res) => {
    try {
        const [produitFromMySQL] = await pool.query('SELECT * FROM Produits WHERE id = ?', [req.params.id]);
        const produitFromMongo = await Produit.findById(req.params.id);

        res.status(200).json({
            mysql: produitFromMySQL[0],
            mongodb: produitFromMongo
        });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// POST - Créer un nouveau produit
exports.createProduit = async (req, res) => {
    try {
        const { nom, description, prix } = req.body;

        const [results] = await pool.query('INSERT INTO Produits (nom, description, prix) VALUES (?, ?, ?)', [nom, description, prix]);
        
        const newProduit = new Produit({ nom, description, prix });
        const savedProduit = await newProduit.save();

        res.status(201).json({ mysqlId: results.insertId, mongoId: savedProduit._id });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// PUT - Mettre à jour un produit par ID
exports.updateProduit = async (req, res) => {
    try {
        const { nom, description, prix } = req.body;

        await pool.query('UPDATE Produits SET nom = ?, description = ?, prix = ? WHERE id = ?', [nom, description, prix, req.params.id]);
        await Produit.updateOne({ _id: req.params.id }, { nom, description, prix });

        res.status(200).send("Updated successfully!");
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// DELETE - Supprimer un produit par ID
exports.deleteProduit = async (req, res) => {
    try {
        await pool.query('DELETE FROM Produits WHERE id = ?', [req.params.id]);
        await Produit.deleteOne({ _id: req.params.id });

        res.status(200).send("Deleted successfully!");
    } catch (error) {
        res.status(500).send(error.message);
    }
};
