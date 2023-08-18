const { pool } = require('../config/database'); 
const { Fournisseur } = require('../models/Fournisseurs');

// CREATE - POST
exports.createFournisseur = async (req, res) => {
    try {
        const { nom, contact, adresse } = req.body;
        
        // Insert into MySQL
        const [results] = await pool.query('INSERT INTO Fournisseurs (nom, contact, adresse) VALUES (?, ?, ?)', [nom, contact, adresse]);
        
        // Insert into MongoDB
        const newFournisseur = new Fournisseur({ nom, contact, adresse });
        const savedFournisseur = await newFournisseur.save();

        res.status(201).json({ mysqlId: results.insertId, mongoId: savedFournisseur._id });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// READ - GET all fournisseurs
exports.getFournisseurs = async (req, res) => {
    try {
        // Fetch from MySQL
        const [results] = await pool.query('SELECT * FROM Fournisseurs');
        
        // Fetch from MongoDB
        const fournisseursFromMongo = await Fournisseur.find();

        res.status(200).json({ mysqlData: results, mongoData: fournisseursFromMongo });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// READ - GET a specific fournisseur by ID
exports.getFournisseurById = async (req, res) => {
    try {
        // Fetch from MySQL
        const [results] = await pool.query('SELECT * FROM Fournisseurs WHERE id = ?', [req.params.id]);

        // Fetch from MongoDB
        const fournisseurFromMongo = await Fournisseur.findById(req.params.id);

        res.status(200).json({ mysqlData: results, mongoData: fournisseurFromMongo });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// UPDATE - PUT
exports.updateFournisseur = async (req, res) => {
    try {
        const { nom, contact, adresse } = req.body;

        // Update MySQL
        await pool.query('UPDATE Fournisseurs SET nom = ?, contact = ?, adresse = ? WHERE id = ?', [nom, contact, adresse, req.params.id]);

        // Update MongoDB
        await Fournisseur.updateOne({ _id: req.params.id }, { nom, contact, adresse });

        res.status(200).send("Updated successfully!");
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// DELETE
exports.deleteFournisseur = async (req, res) => {
    try {
        // Delete from MySQL
        await pool.query('DELETE FROM Fournisseurs WHERE id = ?', [req.params.id]);

        // Delete from MongoDB
        await Fournisseur.deleteOne({ _id: req.params.id });

        res.status(200).send("Deleted successfully!");
    } catch (error) {
        res.status(500).send(error.message);
    }
};
