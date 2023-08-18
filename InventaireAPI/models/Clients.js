const mongoose = require('mongoose');

const clientSchema = new mongoose.Schema({
    nom: {
        type: String,
        required: true,
        trim: true
    },
    adresse: {
        type: String,
        trim: true
    },
    contact: {
        type: String,
        trim: true
    }
});

const Client = mongoose.model('Client', clientSchema);

module.exports = Client;
