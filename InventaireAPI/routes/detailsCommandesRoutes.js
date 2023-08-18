const express = require('express');
const router = express.Router();
const detailsCommandeController = require('../controllers/DetailsCommandeController');

// Get all DetailsCommande
router.get('/', detailsCommandeController.getAllDetailsCommande);

// Get a single DetailsCommande by ID
router.get('/:id', detailsCommandeController.getDetailByCommandeId);

// Create a new DetailsCommande
router.post('/', detailsCommandeController.createDetailCommande);

// Update a DetailsCommande by ID
router.put('/:id', detailsCommandeController.updateDetailCommande);

// Delete a DetailsCommande by ID
router.delete('/:id', detailsCommandeController.deleteDetailCommande);

module.exports = router;
