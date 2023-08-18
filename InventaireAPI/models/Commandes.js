const mongoose = require('mongoose');

const CommandeSchema = new mongoose.Schema({
    client_id: {
        type: mongoose.Schema.Types.ObjectId, // Si vous stockez les IDs des clients en tant qu'ObjectIDs dans MongoDB
        required: true,
        ref: 'Client'  // Si vous avez un modèle 'Client' et souhaitez établir une relation
    },
    date_commande: {
        type: Date,
        required: true
    }
});

module.exports = mongoose.model('Commande', CommandeSchema);
