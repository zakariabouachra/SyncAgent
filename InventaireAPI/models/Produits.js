const mongoose = require('mongoose');

const produitSchema = new mongoose.Schema({
    nom: {
        type: String,
        required: true,
        trim: true,
        maxlength: 255
    },
    description: {
        type: String,
        trim: true,
        maxlength: 1024
    },
    prix: {
        type: Number,
        required: true,
        min: 0
    }
}, {
    timestamps: true  // cela ajoute automatiquement les champs createdAt et updatedAt
});

module.exports = mongoose.model('Produit', produitSchema);
