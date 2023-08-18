const mongoose = require('mongoose');

const historiqueSchema = new mongoose.Schema({
    description: {
        type: String,
        required: true
    },
    date: {
        type: Date,
        required: true,
        default: Date.now
    },
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',  // Si vous avez un modèle d'utilisateur nommé 'User'
        required: true
    }
});

module.exports = mongoose.model('Historique', historiqueSchema);


