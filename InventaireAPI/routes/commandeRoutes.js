const express = require('express');
const router = express.Router();
const commandesController = require('../controllers/commandesController');

// GET - Retrieve all commandes
router.get('/', commandesController.getAllCommandes);

// GET - Retrieve a single commande by ID
router.get('/:id', commandesController.getCommandeById);

// POST - Create a new commande
router.post('/', commandesController.createCommande);

// PUT - Update a commande by ID
router.put('/:id', commandesController.updateCommande);

// DELETE - Delete a commande by ID
router.delete('/:id', commandesController.deleteCommande);

module.exports = router;
