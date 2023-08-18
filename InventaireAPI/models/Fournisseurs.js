const mongoose = require('mongoose');

const fournisseurSchema = new mongoose.Schema({
    nom: {
        type: String,
        required: true,
        trim: true,
        maxlength: 255
    },
    contact: {
        type: String,
        trim: true,
        maxlength: 255
    },
    adresse: {
        type: String,
        trim: true
    }
}, {
    timestamps: true  // Ceci ajoutera automatiquement les champs createdAt et updatedAt à votre modèle
});

const Fournisseur = mongoose.model('Fournisseur', fournisseurSchema);

module.exports = Fournisseur;
