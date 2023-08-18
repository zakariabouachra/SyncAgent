const mysql = require('mysql2/promise');

const pool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'InventaireDB',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

// Vérification de la connexion à la base de données
pool.getConnection()
    .then(connection => {
        console.log('Connexion à la base de données MySQL réussie!');
        connection.release(); // Libération de la connexion
    })
    .catch(error => {
        console.error('Erreur lors de la connexion à la base de données MySQL:', error.message);
    });

module.exports = {
    pool
};
