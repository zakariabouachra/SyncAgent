const express = require('express');
const router = express.Router();
const historiqueController = require('../controllers/HistoriqueController');

// GET - Récupérer tous les entrées d'historique
router.get('/', historiqueController.getAllHistorique);

// GET - Récupérer une entrée d'historique par son ID
router.get('/:id', historiqueController.getHistoriqueById);

// POST - Créer une nouvelle entrée d'historique
router.post('/', historiqueController.createHistoriqueEntry);

// PUT - Mettre à jour une entrée d'historique par son ID
router.put('/:id', historiqueController.updateHistorique);

// DELETE - Supprimer une entrée d'historique par son ID
router.delete('/:id', historiqueController.deleteHistoriqueEntry);

module.exports = router;
