const express = require('express');
const mongoose = require('mongoose');

const fournisseursRoutes = require('./routes/fournisseursRoutes');
const clientsRoutes = require('./routes/ClientsRoutes');
const commandesRoutes = require('./routes/commandeRoutes');
const detailsCommandesRoutes = require('./routes/detailsCommandesRoutes');
const historiquesRoutes = require('./routes/historiquesRoutes');
const produitsRoutes = require('./routes/produitsRoutes');
const stockRoutes = require('./routes/stockRoutes');

const app = express();
const PORT = 3000;

// Connexion à MongoDB
mongoose.connect('mongodb+srv://zackDB:2311@cluster0.uzwuxhn.mongodb.net/', {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
.then(() => {
    console.log('Connected to MongoDB');
})
.catch(error => {
    console.error('Error connecting to MongoDB:', error.message);
});

// Middleware pour le parsing JSON
app.use(express.json());

// Routes
app.use('/fournisseurs', fournisseursRoutes);
app.use('/clients', clientsRoutes);
app.use('/commandes', commandesRoutes);
app.use('/details-commandes', detailsCommandesRoutes);
app.use('/historiques', historiquesRoutes);
app.use('/produits', produitsRoutes);
app.use('/stock', stockRoutes);

// Middleware pour gérer les erreurs 404
app.use((req, res, next) => {
    res.status(404).send('Not Found');
});

// Middleware pour gérer les autres erreurs
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something broke!');
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
