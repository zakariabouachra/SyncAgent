const { pool } = require('../config/database');
const Stock = require('../models/Stock'); // Supposons que vous avez un modèle MongoDB pour Stock

// Récupérer tout le stock
exports.getAllStock = async (req, res) => {
    try {
        const [stockFromMySQL] = await pool.query('SELECT * FROM Stock');

        const stockFromMongo = await Stock.find();

        res.status(200).json({
            mysql: stockFromMySQL,
            mongodb: stockFromMongo
        });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// Récupérer la quantité de stock pour un produit spécifique
exports.getStockByProductId = async (req, res) => {
    try {
        const [result] = await pool.query('SELECT * FROM Stock WHERE product_id = ?', [req.params.id]);

        const stockFromMongo = await Stock.findOne({ product_id: req.params.id });

        res.status(200).json({
            mysql: result,
            mongodb: stockFromMongo
        });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// Mettre à jour le stock pour un produit spécifique
exports.updateStockByProductId = async (req, res) => {
    try {
        const { quantity } = req.body;

        await pool.query('UPDATE Stock SET quantity = ? WHERE product_id = ?', [quantity, req.params.id]);

        await Stock.updateOne({ product_id: req.params.id }, { quantity });

        res.status(200).send("Stock updated successfully!");
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// Ajouter une nouvelle entrée de stock (pour un nouveau produit, par exemple)
exports.addStock = async (req, res) => {
    try {
        const { product_id, quantity } = req.body;

        const [result] = await pool.query('INSERT INTO Stock (product_id, quantity) VALUES (?, ?)', [product_id, quantity]);

        const newStockEntry = new Stock({ product_id, quantity });
        await newStockEntry.save();

        res.status(201).json({ mysqlId: result.insertId, mongoId: newStockEntry._id });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// Supprimer une entrée de stock
exports.deleteStockByProductId = async (req, res) => {
    try {
        await pool.query('DELETE FROM Stock WHERE product_id = ?', [req.params.id]);
        
        await Stock.deleteOne({ product_id: req.params.id });

        res.status(200).send("Stock entry deleted successfully!");
    } catch (error) {
        res.status(500).send(error.message);
    }
};
