const { pool } = require('../config/database'); 
const Commande = require('../models/Commandes'); // Assurez-vous d'avoir un modèle MongoDB approprié

exports.getAllCommandes = async (req, res) => {
    try {
        // Fetch from MySQL
        const [rows] = await pool.query('SELECT * FROM Commandes');
        
        // Fetch from MongoDB
        const mongoCommandes = await Commande.find();

        res.status(200).json({ mysql: rows, mongodb: mongoCommandes });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

exports.getCommandeById = async (req, res) => {
    try {
        const id = req.params.id;

        // Fetch from MySQL
        const [rows] = await pool.query('SELECT * FROM Commandes WHERE id = ?', [id]);

        // Fetch from MongoDB
        const mongoCommande = await Commande.findById(id);

        res.status(200).json({ mysql: rows[0], mongodb: mongoCommande });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

exports.createCommande = async (req, res) => {
    try {
        const { client_id, date_commande } = req.body;

        // Insert into MySQL
        const [results] = await pool.query('INSERT INTO Commandes (client_id, date_commande) VALUES (?, ?)', [client_id, date_commande]);

        // Insert into MongoDB
        const newCommande = new Commande({ client_id, date_commande });
        const savedCommande = await newCommande.save();

        res.status(201).json({ mysqlId: results.insertId, mongoId: savedCommande._id });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

exports.updateCommande = async (req, res) => {
    try {
        const id = req.params.id;
        const { client_id, date_commande } = req.body;

        // Update MySQL
        await pool.query('UPDATE Commandes SET client_id = ?, date_commande = ? WHERE id = ?', [client_id, date_commande, id]);

        // Update MongoDB
        await Commande.updateOne({ _id: id }, { client_id, date_commande });

        res.status(200).send("Updated successfully!");
    } catch (error) {
        res.status(500).send(error.message);
    }
};

exports.deleteCommande = async (req, res) => {
    try {
        const id = req.params.id;

        // Delete from MySQL
        await pool.query('DELETE FROM Commandes WHERE id = ?', [id]);

        // Delete from MongoDB
        await Commande.deleteOne({ _id: id });

        res.status(200).send("Deleted successfully!");
    } catch (error) {
        res.status(500).send(error.message);
    }
};
