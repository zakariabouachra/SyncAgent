const express = require('express');
const router = express.Router();
const clientsController = require('../controllers/clientsController');

// GET - Récupérer tous les clients
router.get('/', clientsController.getAllClients);

// GET - Récupérer un client spécifique par ID
router.get('/:id', clientsController.getClientById);

// POST - Créer un nouveau client
router.post('/', clientsController.createClient);

// PUT - Mettre à jour un client par ID
router.put('/:id', clientsController.updateClient);

// DELETE - Supprimer un client par ID
router.delete('/:id', clientsController.deleteClient);

module.exports = router;
