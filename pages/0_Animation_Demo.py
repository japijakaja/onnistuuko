# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
from typing import Any

import numpy as np

import streamlit as st
from streamlit.hello.utils import show_code


def animation_demo() -> None:

    # Interactive Streamlit elements, like these sliders, return their value.
    # This gives you an extremely simple interaction model.
    iterations = st.sidebar.slider("Level of detail", 2, 20, 10, 1)
    separation = st.sidebar.slider("Separation", 0.7, 2.0, 0.7885)

    # Non-interactive elements return a placeholder to their location
    # in the app. Here we're storing progress_bar to update it later.
    progress_bar = st.sidebar.progress(0)

    # These two elements will be filled in later, so we create a placeholder
    # for them using st.empty()
    frame_text = st.sidebar.empty()
    image = st.empty()

    m, n, s = 960, 640, 400
    x = np.linspace(-m / s, m / s, num=m).reshape((1, m))
    y = np.linspace(-n / s, n / s, num=n).reshape((n, 1))

    for frame_num, a in enumerate(np.linspace(0.0, 4 * np.pi, 100)):
        # Here were setting value for these two elements.
        progress_bar.progress(frame_num)
        frame_text.text("Frame %i/100" % (frame_num + 1))

        # Performing some fractal wizardry.
        c = separation * np.exp(1j * a)
        Z = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
        C = np.full((n, m), c)
        M: Any = np.full((n, m), True, dtype=bool)
        N = np.zeros((n, m))

        for i in range(iterations):
            Z[M] = Z[M] * Z[M] + C[M]
            M[np.abs(Z) > 2] = False
            N[M] = i

        # Update the image placeholder by calling the image() function on it.
        image.image(1.0 - (N / N.max()), use_column_width=True)

    # We clear elements by calling empty on them.
    progress_bar.empty()
    frame_text.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


st.set_page_config(page_title="Animation Demo", page_icon="📹")
st.markdown("# Animation Demo")
st.sidebar.header("Animation Demo")
st.write(
    """This app shows how you can use Streamlit to build cool animations.
It displays an animated fractal based on the the Julia Set. Use the slider
to tune different parameters."""
)

animation_demo()

show_code(animation_demo)
"""

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

# Get user input for player registration
player_name_input = st.text_input("Enter player name:")
team_name_input = st.text_input("Enter team name:")

# Register new player
if st.button("Register Player"):
    insert_player_data(player_name_input, team_name_input)
    st.success(f"Player {player_name_input} registered successfully for team {team_name_input}!")

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





