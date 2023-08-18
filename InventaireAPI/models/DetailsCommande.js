const mongoose = require('mongoose');
const { pool } = require('../config/database');

// MySQL Schema
// Pour MySQL, nous utilisons principalement SQL directement dans le contrôleur, donc nous n'avons pas de "schéma" défini comme avec Mongoose pour MongoDB. Mais pour une meilleure organisation, vous pourriez envisager d'utiliser un ORM comme Sequelize à l'avenir.

// MongoDB Schema
const DetailsCommandeSchema = new mongoose.Schema({
    commande_id: {
        type: Number,
        required: true
    },
    produit_id: {
        type: Number,
        required: true
    },
    quantite: {
        type: Number,
        required: true
    }
});

// MongoDB Model
const DetailsCommande = mongoose.model('DetailsCommande', DetailsCommandeSchema);

module.exports = DetailsCommande;
