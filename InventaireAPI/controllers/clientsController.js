const { pool } = require('../config/database'); 
const Client = require('../models/Clients');

// GET - Retrieve all clients
exports.getAllClients = async (req, res) => {
    try {
        // From MySQL
        const [clientsFromMySQL] = await pool.query('SELECT * FROM Clients');

        // From MongoDB
        const clientsFromMongo = await Client.find();

        res.status(200).json({
            mysql: clientsFromMySQL,
            mongodb: clientsFromMongo
        });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// GET - Retrieve a specific client by ID
exports.getClientById = async (req, res) => {
    try {
        // From MySQL
        const [clientFromMySQL] = await pool.query('SELECT * FROM Clients WHERE id = ?', [req.params.id]);

        // From MongoDB
        const clientFromMongo = await Client.findById(req.params.id);

        res.status(200).json({
            mysql: clientFromMySQL,
            mongodb: clientFromMongo
        });
    } catch (error) {
        res.status(500).send(error.message);
    }
};


// CREATE - POST
exports.createClient = async (req, res) => {
    try {
        const { nom, adresse, contact } = req.body;

        // Insert into MySQL
        const [results] = await pool.query('INSERT INTO Clients (nom, adresse, contact) VALUES (?, ?, ?)', [nom, adresse, contact]);

        // Insert into MongoDB
        const newClient = new Client({ nom, adresse, contact });
        const savedClient = await newClient.save();

        res.status(201).json({ mysqlId: results.insertId, mongoId: savedClient._id });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// UPDATE - PUT
exports.updateClient = async (req, res) => {
    try {
        const { nom, adresse, contact } = req.body;

        // Update MySQL
        await pool.query('UPDATE Clients SET nom = ?, adresse = ?, contact = ? WHERE id = ?', [nom, adresse, contact, req.params.id]);

        // Update MongoDB
        await Client.updateOne({ _id: req.params.id }, { nom, adresse, contact });

        res.status(200).send("Updated successfully!");
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// DELETE
exports.deleteClient = async (req, res) => {
    try {
        // Delete from MySQL
        await pool.query('DELETE FROM Clients WHERE id = ?', [req.params.id]);

        // Delete from MongoDB
        await Client.deleteOne({ _id: req.params.id });

        res.status(200).send("Deleted successfully!");
    } catch (error) {
        res.status(500).send(error.message);
    }
};
