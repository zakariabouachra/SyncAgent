const express = require('express');
const router = express.Router();
const produitsController = require('../controllers/produitsController');

// Récupérer tous les produits
router.get('/', produitsController.getAllProduits);

// Récupérer un produit spécifique par ID
router.get('/:id', produitsController.getProduitById);

// Créer un nouveau produit
router.post('/', produitsController.createProduit);

// Mettre à jour un produit spécifique par ID
router.put('/:id', produitsController.updateProduit);

// Supprimer un produit spécifique par ID
router.delete('/:id', produitsController.deleteProduit);

module.exports = router;
