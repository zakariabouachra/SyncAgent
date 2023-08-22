import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import requests

API_ENDPOINT = 'http://127.0.0.1:5000'

st.set_page_config(
    page_title="Magasin App",
    page_icon="🛍",
    layout="wide",
    initial_sidebar_state="expanded",
)

def get_items(table_name):
    response = requests.get(f"{API_ENDPOINT}/{table_name}")
    if response.status_code == 200:
        return response.json()
    else:
        st.warning(response.text)
        return []

def get_single_item(table_name, item_id):
    response = requests.get(f"{API_ENDPOINT}/{table_name}/{item_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_item(table_name, data):
    response = requests.post(f"{API_ENDPOINT}/{table_name}", json=data)
    return response.text

def update_item(table_name, item_id, data):
    response = requests.put(f"{API_ENDPOINT}/{table_name}/{item_id}", json=data)
    return response.text

def delete_item(table_name, item_id):
    response = requests.delete(f"{API_ENDPOINT}/{table_name}/{item_id}")
    return response.text

def display_dashboard():
    st.header("Dashboard 📊")
    
    display_stock_chart()
    top_sold_products()
    sales_over_time()

def top_sold_products():
    # Supposons que votre table "Historique" a une colonne "Action" où la valeur "Vente" indique une vente
    sales = get_items("Historique")
    df_sales = pd.DataFrame(sales)
    top_sales = df_sales[df_sales["Action"] == "Vente"]
    
    # Group by product and sum up the quantity
    top_products = top_sales.groupby("ID_Produit").sum().sort_values("Quantité", ascending=False)
    
    st.header("Produits les plus vendus")
    st.bar_chart(top_products["Quantité"].head(10))  # Top 10 products


def sales_over_time():
    sales = get_items("Historique")
    df_sales = pd.DataFrame(sales)
    sales_over_time = df_sales[df_sales["Action"] == "Vente"].groupby("Date").sum()
    
    st.header("Historique des ventes")
    st.line_chart(sales_over_time["Quantité"])



def display_stock_chart():
    items = get_items("Stock")
    df = pd.DataFrame(items)
    st.header("Historique du stock par produit")
    st.line_chart(df.set_index("ID_Produit")["Quantité"])


def notify_low_stock():
    items = get_items("Stock")
    for item in items:
        if int(item["Quantité"]) < 10: 
            st.warning(f"Stock faible pour le produit ID: {item['ID_Produit']}")

def search_items(table_name, query):
    items = get_items(table_name)
    filtered_items = [item for item in items if query.lower() in item.get("Nom_Produit", "").lower()]
    df = pd.DataFrame(filtered_items)
    AgGrid(df)

def display_items(table_name):
    items = get_items(table_name)
    df = pd.DataFrame(items)
    AgGrid(df)

def create_form(table_name, default_data=None):
    form_data = {}

    if not default_data:
        default_data = {}

    if table_name == "Produits":
        form_data["Nom_Produit"] = st.text_input("Nom du produit", value=default_data.get("Nom_Produit", ""))
        form_data["Description"] = st.text_area("Description", value=default_data.get("Description", ""))
        form_data["Prix_Unitaire"] = st.text_input("Prix unitaire", value=default_data.get("Prix_Unitaire", ""))
    
    elif table_name == "Fournisseurs":
        form_data["Nom_Fournisseur"] = st.text_input("Nom du fournisseur", value=default_data.get("Nom_Fournisseur", ""))
        form_data["Adresse"] = st.text_input("Adresse", value=default_data.get("Adresse", ""))
        form_data["Téléphone"] = st.text_input("Téléphone", value=default_data.get("Téléphone", ""))
    
    elif table_name == "Stock":
        form_data["ID_Produit"] = st.text_input("ID Produit", value=default_data.get("ID_Produit", ""))
        form_data["Quantité"] = st.text_input("Quantité", value=default_data.get("Quantité", ""))
    
    elif table_name == "Historique":
        form_data["ID_Produit"] = st.text_input("ID Produit", value=default_data.get("ID_Produit", ""))
        form_data["Date"] = st.date_input("Date", value=default_data.get("Date", pd.to_datetime('today'))).strftime('%Y-%m-%d')
        form_data["Action"] = st.radio("Action", ['Achat', 'Vente'], index=0 if default_data.get("Action", "") == "Achat" else 1)
        form_data["Quantité"] = st.text_input("Quantité", value=default_data.get("Quantité", ""))
    
    elif table_name == "Clients":
        form_data["Nom_Client"] = st.text_input("Nom du client", value=default_data.get("Nom_Client", ""))
        form_data["Prénom_Client"] = st.text_input("Prénom du client", value=default_data.get("Prénom_Client", ""))
        form_data["Email"] = st.text_input("Email", value=default_data.get("Email", ""))
        form_data["Adresse"] = st.text_input("Adresse", value=default_data.get("Adresse", ""))
        form_data["Téléphone"] = st.text_input("Téléphone", value=default_data.get("Téléphone", ""))
        form_data["Date_Inscription"] = st.date_input("Date d'inscription", value=default_data.get("Date_Inscription", pd.to_datetime('today')))

    if st.button("Soumettre"):
        return form_data
    else:
        return None

def get_id_and_name_from_item(table_name, item):
    if table_name == "Produits":
        return str(item["ID_Produit"]), item["Nom_Produit"]
    elif table_name == "Fournisseurs":
        return str(item["ID_Fournisseur"]), item["Nom_Fournisseur"]
    elif table_name == "Stock":
        return str(item["ID_Stock"]), {item['Nom_Produit']}
    elif table_name == "Historique":
        return str(item["ID_Historique"]), {item['Nom_Produit']}
    elif table_name == "Clients":
        return str(item["ID_Client"]), f"{item['Nom_Client']} {item['Prénom_Client']}"
    else:
        return str(item["ID"]), "Item"  # Un cas par défaut pour toute autre table non mentionnée


def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    password = st.sidebar.text_input("Entrez le mot de passe:", type="password")
    if password == "adminpass":
        st.session_state.authenticated = True
    if not st.session_state.authenticated:
        st.warning("Veuillez vous authentifier pour accéder à l'interface.")
        return

    st.sidebar.header("Options 🛠️")
    table_choice = st.sidebar.selectbox("Tables", ["Produits", "Fournisseurs", "Stock", "Historique", "Clients"])
    operation_choice = st.sidebar.radio("Opérations", ["Dashboard", "Afficher", "Ajouter", "Modifier", "Supprimer"])

    if operation_choice == "Modifier":
        st.subheader(f"Modification des éléments de {table_choice}")

        items = get_items(table_choice)
        item_choices = [f"{get_id_and_name_from_item(table_choice, item)[0]} - {get_id_and_name_from_item(table_choice, item)[1]}" for item in items]
        
        selected_item_desc = st.selectbox("Sélectionnez l'élément à modifier:", item_choices)
        selected_item_id = selected_item_desc.split(" - ")[0]
        item = get_single_item(table_choice, selected_item_id)

        if item:
            data = create_form(table_choice, default_data=item)
            if data:
                response = update_item(table_choice, selected_item_id, data)
                st.success(f"Élément modifié avec succès! Réponse: {response} ✅")

    elif operation_choice == "Supprimer":
        st.subheader(f"Suppression des éléments de {table_choice}")

        items = get_items(table_choice)
        item_choices = [f"{get_id_and_name_from_item(table_choice, item)[0]} - {get_id_and_name_from_item(table_choice, item)[1]}" for item in items]
        
        selected_item_desc = st.selectbox("Sélectionnez l'élément à supprimer:", item_choices)
        selected_item_id = selected_item_desc.split(" - ")[0]

        if st.button("Supprimer 🗑️"):
            response = delete_item(table_choice, selected_item_id)
            st.success(f"Élément supprimé avec succès! Réponse: {response} ✅")
    elif operation_choice == "Afficher":
        st.subheader(f"Affichage des éléments de {table_choice}")
        items = get_items(table_choice)
        for item in items:
            st.write(item)

    elif operation_choice == "Ajouter":
        st.subheader(f"Ajout d'un nouvel élément à {table_choice}")

        # Si l'utilisateur ajoute un élément à la table Stock ou Historique, un choix de produit est nécessaire
        if table_choice in ["Stock", "Historique"]:
            products = get_items("Produits")
            product_choices = [f"{get_id_and_name_from_item('Produits', product)[0]} - {get_id_and_name_from_item('Produits', product)[1]}" for product in products]
            selected_product_desc = st.selectbox("Sélectionnez un produit:", product_choices)
            selected_product_id = selected_product_desc.split(" - ")[0]
            data = create_form(table_choice, default_data={"ID_Produit": int(selected_product_id)})
        else:
            data = create_form(table_choice)
        
        if data:
            response = create_item(table_choice, data)
            st.success(f"Élément ajouté avec succès! Réponse: {response} ✅")
    else: 
        display_dashboard()
    
    # Ajoutez ici les autres options d'opération...

    st.write("---")
    st.write("Magasin App © 2023")

if __name__ == "__main__":
    main()

