const express = require('express');
const router = express.Router();
const stockController = require('../controllers/stockController');

// Récupérer tous les stocks
router.get('/', stockController.getAllStock);

// Récupérer le stock d'un produit spécifique par ID
router.get('/:id', stockController.getStockByProductId);

// Créer un nouveau stock pour un produit
router.post('/', stockController.addStock);

// Mettre à jour le stock d'un produit spécifique par ID
router.put('/:id', stockController.updateStockByProductId);

// Supprimer le stock d'un produit spécifique par ID
router.delete('/:id', stockController.deleteStockByProductId);

module.exports = router;
