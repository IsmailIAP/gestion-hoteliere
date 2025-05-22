import sqlite3
import pandas as pd

conn = sqlite3.connect('Gestion_Hotel.db', check_same_thread=False)
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

def get_reservations():
    return pd.read_sql_query("SELECT * FROM Reservation", conn)

def get_clients():
    return pd.read_sql_query("SELECT * FROM Client", conn)

def chambres_disponibles(date_debut, date_fin):
    query = """
    SELECT Id_Chambre FROM Chambre WHERE Id_Chambre NOT IN (
        SELECT Chambre.Id_Chambre FROM Chambre
        JOIN Type_Chambre ON Chambre.Id_Type = Type_Chambre.Id_Type
        JOIN Concerne ON Type_Chambre.Id_Type = Concerne.Id_Type
        JOIN Reservation ON Concerne.Id_Reservation = Reservation.Id_Reservation
        WHERE NOT (Date_depart <= ? OR Date_arrivee >= ?)
    )
    """
    return pd.read_sql_query(query, conn, params=(date_debut, date_fin))

def insert_client(id_client, adresse, ville, code_postal, email, telephone, nom_complet):
    cursor.execute("""
        INSERT INTO Client (Id_Client, Adresse, Ville, Code_postal, E_mail, N_telephone, Nom_complet)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (id_client, adresse, ville, code_postal, email, telephone, nom_complet))
    conn.commit()

def insert_reservation(id_reservation, date_arrivee, date_depart, id_client):
    cursor.execute("""
        INSERT INTO Reservation (Id_Reservation, Date_arrivee, Date_depart, Id_Client)
        VALUES (?, ?, ?, ?)
    """, (id_reservation, date_arrivee, date_depart, id_client))
    conn.commit()