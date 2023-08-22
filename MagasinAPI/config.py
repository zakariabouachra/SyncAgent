from flask import Flask
from flask_mysqldb import MySQL , MySQLdb
from pymongo import MongoClient


app = Flask(__name__)

# Configuration MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Magasin'

with app.app_context():
    try:
        mysql = MySQL(app)
        conn = mysql.connection
        if conn :
            print("Connexion à MySQL réussie!")
    except MySQLdb.MySQLError as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")



try:
    client = MongoClient("mongodb+srv://zackDB:2311@cluster0.uzwuxhn.mongodb.net/")
    if client:
        mongo_db = client['Magasin']
        print("Connexion à MongoDB réussie!")
    else:
        print("Erreur lors de la connexion à MongoDB: l'objet 'db' est None")
except Exception as e:
    print(f"Erreur lors de la connexion à MongoDB: {e}")

try:
    TABLES = mongo_db.list_collection_names()
    print(f"Tables/Collections détectées: {', '.join(TABLES)}")
except Exception as e:
    print(f"Erreur lors de la récupération des collections de MongoDB: {e}")
    TABLES = []