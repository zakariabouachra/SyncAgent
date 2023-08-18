const mongoose = require('mongoose');

const stockSchema = new mongoose.Schema({
    product_id: {
        type: String,
        required: true,
        unique: true
    },
    quantity: {
        type: Number,
        required: true
    }
});

module.exports = mongoose.model('Stock', stockSchema);
