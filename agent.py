import threading
from pymongo import MongoClient
import mysql.connector
import time
import requests
import datetime
import json


config = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "database": "Magasin",
    "raise_on_warnings": True
}

def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def notify_api_about_change(change):

    api_endpoint = "http://127.0.0.1:5000/notify_change"
    
    # Convert the data to a JSON string
    data_as_json = json.dumps(change, default=datetime_converter)

    try:
        headers = {'Content-type': 'application/json'}
        response = requests.post(api_endpoint, data=data_as_json, headers=headers)
        
        if response.status_code == 200:
            print("Notification à l'API réussie!")
        else:
            print(f"Erreur lors de la notification à l'API: {response.status_code}")
    except requests.RequestException as e:
        print(f"Erreur lors de la notification à l'API: {e}")



def watch_collection(collection_name):
    collection = db[collection_name]
    with collection.watch() as stream:
        for change in stream:
            print(f"Reçu changement de type: {change['operationType']} dans la collection {collection_name}")

            data_payload = {
                "operation": change["operationType"],
                "data": change.get("fullDocument", {}),
                "changes": change.get("updateDescription", {}).get("updatedFields", {}),
                "database_type": "MongoDB",
                "collection_name": collection_name,
                "id":change['documentKey']['_id']
            }

            notify_api_about_change(data_payload)
            print(data_payload)


def watch_mysql():
  

    last_id = 0
    try:
        while True:
            connection = mysql.connector.connect(**config)
            last_id = get_latest_changes(connection, last_id)
            connection.close()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Surveillance MySQL arrêtée.")
    finally:
        connection.close()

def get_latest_changes(connection, last_id=0):
    cursor = connection.cursor(dictionary=True, buffered=False)
    try:
        query = "SELECT * FROM audit_table WHERE ID > %s ORDER BY timestamp DESC"
        cursor.execute(query, (last_id,))
        rows = cursor.fetchall()

        if rows:
            last_id = rows[0]["ID"]
            for row in rows:
                change = {
                    "action": row['action'],
                    "table_name": row['table_name'],
                    "record_id": row['record_id'],
                    "timestamp": row['timestamp'],
                    "database_type": "MySQL"
                }

                # Fetch actual data change if necessary
                actual_data = fetch_actual_data(row)
                change["actual_data"] = actual_data

                notify_api_about_change(change)
                print(f"Action: {row['action']}, Table: {row['table_name']}, Record ID: {row['record_id']}, Timestamp: {row['timestamp']}")
                # Delete the processed rows from the audit_table
            delete_query = "DELETE FROM audit_table WHERE ID <= %s"
            cursor.execute(delete_query, (last_id,))
            connection.commit()

        return last_id
    except mysql.connector.Error as err:
        print(f"Erreur SQL: {err}")
    finally:
        cursor.close()
# Define a mapping of table names to their respective primary key columns
table_to_primary_key = {
    'Produits': 'ID_Produit',
    'Fournisseurs': 'ID_Fournisseur',
    'Stock': 'ID_Stock',
    'Historique': 'ID_Historique',
    'Clients': 'ID_Client'
}

def fetch_actual_data(row):
    data = {}
    connection = mysql.connector.connect(**config) 
    cursor = connection.cursor(dictionary=True)

    # Fetch the primary key column for the table from the dictionary
    primary_key_column = table_to_primary_key.get(row['table_name']) 

    # If the table name doesn't exist in the dictionary, raise an error
    if not primary_key_column:
        raise ValueError(f"Table {row['table_name']} not found in primary key mapping dictionary.")

    query = f"SELECT * FROM {row['table_name']} WHERE {primary_key_column} = %s"
    cursor.execute(query, (row['record_id'],))
    results = cursor.fetchall()
    
    if results:
        data = results[0]

    cursor.close()
    connection.close()

    return data



def main():
    client = MongoClient("mongodb+srv://zackDB:2311@cluster0.uzwuxhn.mongodb.net/")
    global db
    db = client["Magasin"]
    all_collections = db.list_collection_names()

    mongo_threads = []
    for col_name in all_collections:
        t = threading.Thread(target=watch_collection, args=(col_name,))
        t.start()
        mongo_threads.append(t)

    mysql_thread = threading.Thread(target=watch_mysql)
    mysql_thread.start()

    mysql_thread.join()
    for t in mongo_threads:
        t.join()

if __name__ == "__main__":
    main()