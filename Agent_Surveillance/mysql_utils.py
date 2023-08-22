import mysql.connector
import time
import api_utils

config = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "database": "Magasin",
    "raise_on_warnings": True
}

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

                api_utils.notify_api_about_change(change)
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