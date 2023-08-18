const { pool } = require('../config/database');
const Historique = require('../models/Historique');

// GET - Retrieve all historique entries
exports.getAllHistorique = async (req, res) => {
    try {
        // From MySQL
        const [historiqueFromMySQL] = await pool.query('SELECT * FROM Historique');

        // From MongoDB
        const historiqueFromMongo = await Historique.find();

        res.status(200).json({
            mysql: historiqueFromMySQL,
            mongodb: historiqueFromMongo
        });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// GET - Retrieve a single historique entry by ID
exports.getHistoriqueById = async (req, res) => {
    try {
        // From MySQL
        const [entryFromMySQL] = await pool.query('SELECT * FROM Historique WHERE id = ?', [req.params.id]);

        // From MongoDB
        const entryFromMongo = await Historique.findById(req.params.id);

        res.status(200).json({
            mysql: entryFromMySQL,
            mongodb: entryFromMongo
        });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// POST - Create a new historique entry
exports.createHistoriqueEntry = async (req, res) => {
    try {
        const { description, date, userId } = req.body;

        // Insert into MySQL
        const [results] = await pool.query('INSERT INTO Historique (description, date, userId) VALUES (?, ?, ?)', 
                                           [description, date, userId]);

        // Insert into MongoDB
        const newEntry = new Historique({ description, date, userId });
        const savedEntry = await newEntry.save();

        res.status(201).json({ mysqlId: results.insertId, mongoId: savedEntry._id });
    } catch (error) {
        res.status(500).send(error.message);
    }
};

// PUT - Update a historique entry by ID
exports.updateHistorique = async (req, res) => {
    try {
        const { description, date, userId } = req.body;

        // Update in MySQL
        await pool.query('UPDATE Historique SET description = ?, date = ?, userId = ? WHERE id = ?', 
                         [description, date, userId, req.params.id]);

        // Update in MongoDB
        const updatedEntry = await Historique.findByIdAndUpdate(req.params.id, { description, date, userId }, { new: true });

        res.status(200).json({ mysql: "Updated successfully!", mongodb: updatedEntry });
    } catch (error) {
        res.status(500).send(error.message);
    }
};


// DELETE - Delete a historique entry by ID
exports.deleteHistoriqueEntry = async (req, res) => {
    try {
        // Delete from MySQL
        await pool.query('DELETE FROM Historique WHERE id = ?', [req.params.id]);

        // Delete from MongoDB
        await Historique.deleteOne({ _id: req.params.id });

        res.status(200).send("Deleted successfully!");
    } catch (error) {
        res.status(500).send(error.message);
    }
};
