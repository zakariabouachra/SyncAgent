const express = require('express');
const router = express.Router();
const fournisseurController = require('../controllers/fournisseursController');

// GET - Récupérer tous les fournisseurs
router.get('/', fournisseurController.getFournisseurById);

// GET - Récupérer un fournisseur par son ID
router.get('/:id', fournisseurController.getFournisseurById);

// POST - Créer un nouveau fournisseur
router.post('/', fournisseurController.createFournisseur);

// PUT - Mettre à jour un fournisseur par son ID
router.put('/:id', fournisseurController.updateFournisseur);

// DELETE - Supprimer un fournisseur par son ID
router.delete('/:id', fournisseurController.deleteFournisseur);

module.exports = router;
