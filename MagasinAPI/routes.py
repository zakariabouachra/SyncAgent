from flask import jsonify, request
from config import mysql, mongo_db
from models import SCHEMAS , configs , table_to_primary_key
import mysql.connector as mysql_connector

def init_routes(app):
    @app.route('/<table>', methods=['POST'])
    def create(table):
        if table not in SCHEMAS:
            return jsonify({"message": "Table non trouvée!"}), 404

        item_info = request.json
        fields = SCHEMAS[table]['fields']

        # Assurez-vous que tous les champs nécessaires sont présents
        for field in fields:
            if field not in item_info:
                return jsonify({"message": f"Champ '{field}' manquant!"}), 400

        # MySQL Insertion
        cur = mysql.connection.cursor()
        cur.execute(SCHEMAS[table]['mysql_insert'], tuple(item_info[field] for field in fields))
        mysql.connection.commit()
        #item_id = cur.lastrowid
        cur.close()

        # MongoDB Insertion
        #try:
            #item_info['_id'] = item_id
            #mongo_db[table].insert_one(item_info)
        #except Exception as e:
            #print("Error inserting into MongoDB:", e)
            #return jsonify({"message": "Error inserting into MongoDB"}), 500

        return jsonify({"message": f"{table} ajouté avec succès!"}), 201


    def get_product_details(product_id):
        return mongo_db["Produits"].find_one({"_id": product_id})


    @app.route('/<table>', methods=['GET'])
    def get_all(table):
        if table not in SCHEMAS:
            return jsonify({"message": "Table non trouvée!"}), 404

        cur = mysql.connection.cursor()

        # Si la table a une référence à ID_Produit
        if "ID_Produit" in SCHEMAS[table]["fields"]:
            cur.execute(f"SELECT * FROM {table}")
            items = cur.fetchall()

            # Conversion des résultats en liste de dictionnaires
            field_names = [desc[0] for desc in cur.description]
            items_as_dicts = [dict(zip(field_names, item)) for item in items]

            # Mise à jour des dictionnaires avec les détails des produits depuis MongoDB
            for item in items_as_dicts:
                product_details = get_product_details(item["ID_Produit"])
                if product_details:
                    # Supprimez l'ID_Produit, car nous intégrons les détails du produit
                    del item["ID_Produit"]
                    item.update(product_details)

            cur.close()
            return jsonify(items_as_dicts)
        else:
            # Pour les tables sans référence à ID_Produit
            cur.execute(f"SELECT * FROM {table}")
            items = cur.fetchall()
            field_names = [desc[0] for desc in cur.description]
            items_as_dicts = [dict(zip(field_names, item)) for item in items]
            cur.close()
            return jsonify(items_as_dicts)

    @app.route('/<table>/<int:id>', methods=['GET'])
    def get_one(table, id):
        if table not in SCHEMAS:
            return jsonify({"message": "Table non trouvée!"}), 404

        cur = mysql.connection.cursor()

        primary_key = SCHEMAS[table].get("primary_key")

        # Si la table a une référence à ID_Produit
        if "ID_Produit" in SCHEMAS[table]["fields"]:
            cur.execute(f"SELECT * FROM {table} WHERE {primary_key} = %s", (id,))
            item = cur.fetchone()
        

            if not item:
                cur.close()
                return jsonify({"message": f"Élément non trouvé dans {table}!"}), 404
            
            # Conversion du résultat en dictionnaire
            field_names = [desc[0] for desc in cur.description]
            item_as_dict = dict(zip(field_names, item))

            # Mise à jour du dictionnaire avec les détails du produit depuis MongoDB
            product_details = get_product_details(item_as_dict["ID_Produit"])
            if product_details:
                # Supprimez l'ID_Produit, car nous intégrons les détails du produit
                del item_as_dict["ID_Produit"]
                item_as_dict.update(product_details)

            return jsonify(item_as_dict)

        else:
            # Pour les tables sans référence à ID_Produit
            cur.execute(f"SELECT * FROM {table} WHERE {primary_key} = %s", (id,))
            item = cur.fetchone()
            

            if not item:
                cur.close()
                return jsonify({"message": f"Élément non trouvé dans {table}!"}), 404

            field_names = [desc[0] for desc in cur.description]
            item_as_dict = dict(zip(field_names, item))
            
            return jsonify(item_as_dict)



    @app.route('/<table>/<int:id>', methods=['PUT'])
    def update(table, id):
        if table not in SCHEMAS:
            return jsonify({"message": "Table non trouvée!"}), 404

        item_info = request.json
        cur = mysql.connection.cursor()
        cur.execute(SCHEMAS[table]['mysql_update'], tuple(item_info[field] for field in SCHEMAS[table]['fields']) + (id,))
        mysql.connection.commit()
        cur.close()


        # MongoDB Update
        #mongo_db[table].update_one({"_id": id}, {"$set": item_info})

        return jsonify({"message": f"{table} mis à jour avec succès!"}), 200


    @app.route('/<table>/<int:id>', methods=['DELETE'])
    def delete(table, id):
        if table not in SCHEMAS:
            return jsonify({"message": "Table non trouvée!"}), 404

        # MySQL Suppression
        cur = mysql.connection.cursor()
        cur.execute(SCHEMAS[table]['mysql_delete'], (id,))
        mysql.connection.commit()
        cur.close()


        # MongoDB Suppression
        mongo_db[table].delete_one({"_id": id})

        return jsonify({"message": f"{table} supprimé avec succès!"}), 200

    @app.route('/notify_change', methods=['POST'])
    def notify_change():
        data = request.json

        # Log the change
        print("Notification reçue pour changement:", data)

        # Si le changement provient de MySQL
        if data.get('database_type') == 'MySQL':
            table_name = data["table_name"]
            action = data["action"]
            record_data = data["actual_data"]

            # Trouvez la collection MongoDB correspondante
            collection = mongo_db[table_name]

            if action == "INSERT" or action == "UPDATE":
                existing_data = collection.find_one({"_id": data["record_id"]})
                

                if not existing_data or existing_data != record_data:
                    collection.update_one(
                        {"_id": data["record_id"]},
                        {"$set": record_data},
                        upsert=True
                    )
                    print(f"{action} appliqué à MongoDB pour la table {table_name}")

            elif action == "DELETE":
                existing_data = collection.find_one({"_id": data["record_id"]})

                if existing_data:
                    collection.delete_one({"_id": data["record_id"]})
                    print(f"{action} appliqué à MongoDB pour la table {table_name}")

        elif data.get('database_type') == 'MongoDB':
            table_name = data.get('collection_name')
            action = data.get("operation")
            primary_key = table_to_primary_key.get(table_name, "_id")  # Utilisez le dictionnaire pour obtenir le nom de la colonne d'ID.
            
            if action in ["insert", "update"]:
                record_data = data.get("data") if action == "insert" else data.get("changes")
                
                if not record_data:
                    print(f"Aucune donnée à insérer ou mettre à jour pour l'action '{action}'")
                    return

                record_data.pop('_id', None)  # Supprimez le champ _id
                id = data.get('id', record_data.get(primary_key))  # Obtenez l'ID de data ou, si absent, de record_data.
                record_data[primary_key] = id

                connection = mysql_connector.connect(**configs)
                cursor = connection.cursor(dictionary=True)

                query = f"SELECT * FROM {table_name} WHERE {primary_key} = %s"
                cursor.execute(query, (id,))
                existing_data = cursor.fetchone()

                cols = ', '.join("`" + str(x).replace('/', '_') + "`" for x in record_data.keys())
                vals = tuple(record_data.values())
                placeholders = ', '.join(['%s'] * len(vals))

                if not existing_data:  # Si l'enregistrement n'existe pas, insérez-le.
                    sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
                else:  # Sinon, mettez à jour l'enregistrement existant.
                    assignments = ', '.join(f"`{col}` = %s" for col in record_data.keys())
                    sql = f"UPDATE {table_name} SET {assignments} WHERE {primary_key} = %s"
                    vals += (id,)  # Ajout de l'ID à la fin des valeurs pour la condition WHERE.

                cursor.execute(sql, vals)
                connection.commit()
                print(f"{action} appliqué à MySQL pour la table {table_name}")
                cursor.close()
                connection.close()

            elif action == "delete":
                connection = mysql_connector.connect(**configs)
                cursor = connection.cursor(dictionary=True)
                id = data.get('id')

                if not id:
                    print("Aucun ID fourni pour l'action 'delete'")
                    return

                sql = f"DELETE FROM {table_name} WHERE {primary_key} = %s"
                cursor.execute(sql, (id,))
                connection.commit()
                print(f"{action} appliqué à MySQL pour la table {table_name}")
                cursor.close()
                connection.close()

        return jsonify({"message": "Notification traitée avec succès!"}), 200
