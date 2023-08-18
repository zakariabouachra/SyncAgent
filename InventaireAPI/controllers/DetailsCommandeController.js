const { pool } = require('../config/database');
const DetailsCommande = require('../models/DetailsCommande');

// Retrieve all details of commandes
exports.getAllDetailsCommande = async (req, res) => {
    try {
        const [results] = await pool.query('SELECT * FROM DetailsCommande');
        res.status(200).json(results);
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// Retrieve a single detail by commande ID
exports.getDetailByCommandeId = async (req, res) => {
    try {
        const [results] = await pool.query('SELECT * FROM DetailsCommande WHERE commande_id = ?', [req.params.id]);
        res.status(200).json(results);
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// Create a new detail for a commande
exports.createDetailCommande = async (req, res) => {
    try {
        const { commande_id, produit_id, quantite } = req.body;
        
        // Insert into MySQL
        const [results] = await pool.query('INSERT INTO DetailsCommande (commande_id, produit_id, quantite) VALUES (?, ?, ?)', 
                                           [commande_id, produit_id, quantite]);
        
        res.status(201).json({ id: results.insertId });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// Update detail for a commande by ID
exports.updateDetailCommande = async (req, res) => {
    try {
        const { commande_id, produit_id, quantite } = req.body;

        // Update MySQL
        await pool.query('UPDATE DetailsCommande SET produit_id = ?, quantite = ? WHERE commande_id = ?', 
                         [produit_id, quantite, req.params.id]);

        res.status(200).send("Updated successfully!");
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// Delete detail for a commande by ID
exports.deleteDetailCommande = async (req, res) => {
    try {
        // Delete from MySQL
        await pool.query('DELETE FROM DetailsCommande WHERE commande_id = ?', [req.params.id]);
        
        res.status(200).send("Deleted successfully!");
    } catch (error) {
        res.status(500).send(error.message);
    }
};
