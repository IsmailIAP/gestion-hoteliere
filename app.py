import streamlit as st
from datetime import datetime
import db_utils

st.title("Gestion Hôtelière - Interface")

option = st.sidebar.selectbox("Choisir une action", [
    "Consulter réservations",
    "Consulter clients",
    "Chambres disponibles",
    "Ajouter client",
    "Ajouter réservation"
])

def afficher_reservations():
    df = db_utils.get_reservations()
    st.subheader("Liste des réservations")
    st.dataframe(df)

def afficher_clients():
    df = db_utils.get_clients()
    st.subheader("Liste des clients")
    st.dataframe(df)

def afficher_chambres_disponibles():
    st.subheader("Recherche chambres disponibles")
    date_debut = st.date_input("Date début")
    date_fin = st.date_input("Date fin")
    if date_fin < date_debut:
        st.error("La date de fin doit être supérieure à la date de début.")
        return
    
    if st.button("Rechercher"):
        df = db_utils.chambres_disponibles(date_debut.strftime("%Y-%m-%d"), date_fin.strftime("%Y-%m-%d"))
        if df.empty:
            st.write("Aucune chambre disponible pour cette période.")
        else:
            st.write(f"Chambres disponibles du {date_debut} au {date_fin} :")
            st.dataframe(df)

def ajouter_client():
    st.subheader("Ajouter un client")
    id_client = st.number_input("ID Client", min_value=1, step=1)
    adresse = st.text_input("Adresse")
    ville = st.text_input("Ville")
    code_postal = st.text_input("Code postal")
    email = st.text_input("E-mail")
    telephone = st.text_input("Téléphone")
    nom_complet = st.text_input("Nom complet")
    
    if st.button("Ajouter client"):
        try:
            db_utils.insert_client(id_client, adresse, ville, code_postal, email, telephone, nom_complet)
            st.success("Client ajouté avec succès.")
        except Exception as e:
            st.error(f"Erreur : {e}")

def ajouter_reservation():
    st.subheader("Ajouter une réservation")
    id_reservation = st.number_input("ID Réservation", min_value=1, step=1)
    date_arrivee = st.date_input("Date arrivée")
    date_depart = st.date_input("Date départ")
    id_client = st.number_input("ID Client", min_value=1, step=1)
    
    if date_depart < date_arrivee:
        st.error("La date de départ doit être après la date d'arrivée.")
        return
    
    if st.button("Ajouter réservation"):
        try:
            db_utils.insert_reservation(id_reservation, date_arrivee.strftime("%Y-%m-%d"), date_depart.strftime("%Y-%m-%d"), id_client)
            st.success("Réservation ajoutée avec succès.")
        except Exception as e:
            st.error(f"Erreur : {e}")

if option == "Consulter réservations":
    afficher_reservations()
elif option == "Consulter clients":
    afficher_clients()
elif option == "Chambres disponibles":
    afficher_chambres_disponibles()
elif option == "Ajouter client":
    ajouter_client()
elif option == "Ajouter réservation":
    ajouter_reservation()