# -*- coding: utf-8 -*-


import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect("training_database.db", check_same_thread=False)
cursor = conn.cursor()

# Create players table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT,
        team_name TEXT
    )
''')
conn.commit()

# Create participants table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS participants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT,
        team_name TEXT,
        training_day TEXT
    )
''')
conn.commit()

# Streamlit app
st.title("Lisää laskijoita valmennusryhmiin")

# Function to insert player data into the players table
def insert_player_data(player_name, team_name):
    cursor.execute('''
        INSERT INTO players (player_name, team_name) VALUES (?, ?)
    ''', (player_name, team_name))
    conn.commit()

# Function to insert participant data into the participants table
def insert_participant_data(player_name, team_name, training_day):
    cursor.execute('''
        INSERT INTO participants (player_name, team_name, training_day) VALUES (?, ?, ?)
    ''', (player_name, team_name, training_day))
    conn.commit()

# Get user input for player registration
player_name_input = st.text_input("Syötä laskijan (etu)nimi:")
team_name_input = st.text_input("Syötä valmennusryhmä:")

# Register new player
if st.button("Lisää laskija"):
    insert_player_data(player_name_input, team_name_input)
    st.success(f"Laskija {player_name_input} rekisteröitiin onnistunesti ryhmään {team_name_input}!")


#näytetään syötetyt laskijat

# Read data from participants table into a Pandas DataFrame
query = 'SELECT * FROM players'
players_df = pd.read_sql_query(query, conn, coerce_float=False)

# Display the DataFrame in Streamlit
st.divider()
st.subheader("Tähän mennessä lisätyt laskijat ja valmentajat:")
st.dataframe(players_df)


# Close the database connection
conn.close()
