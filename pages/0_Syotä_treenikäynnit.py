
# TÄSTÄ ALKAA


import streamlit as st
import sqlite3
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
st.title("Training Scheduler App")

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

# Display the player list for each team
teams = cursor.execute('SELECT DISTINCT team_name FROM players').fetchall()
teams = [team[0] for team in teams]  # Extracting team names from tuples
selected_team = st.selectbox("Select Team:", teams)

# Get player names for the selected team
players_for_team = cursor.execute('SELECT player_name FROM players WHERE team_name = ?', (selected_team,)).fetchall()
players_for_team = [player[0] for player in players_for_team]

# Checkbox list for player selection
selected_players = st.multiselect("Select Players:", players_for_team)

# Select training day
training_day = st.date_input("Select Training Day:")

# Save button for participant registration
if st.button("Register Participants"):
    for player in selected_players:
        insert_participant_data(player, selected_team, training_day.strftime("%Y-%m-%d"))
    st.success("Participants registered successfully!")

# Close the database connection
conn.close()





