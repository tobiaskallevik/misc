import json
import sqlite3

# Step 1: Load JSON data
with open('games.json', 'r') as file:
    games_data = json.load(file)

# Step 2: Create SQLite database and tables
conn = sqlite3.connect('games.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    first_release_date INTEGER,
                    rating REAL,
                    rating_count INTEGER,
                    slug TEXT,
                    summary TEXT,
                    cover_url TEXT)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS game_companies (
    game_id INTEGER, 
    company_id INTEGER, 
    PRIMARY KEY (game_id, company_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS game_modes (
    game_id INTEGER,
    mode_id INTEGER,
    PRIMARY KEY (game_id, mode_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS game_themes (
    game_id INTEGER, 
    theme_id INTEGER, 
    PRIMARY KEY (game_id, theme_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS game_engines (
    game_id INTEGER, 
    engine_id INTEGER, 
    PRIMARY KEY (game_id, engine_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS game_genres (
    game_id INTEGER, 
    genre_id INTEGER, 
    PRIMARY KEY (game_id, genre_id)
)
''')

# Step 3: Insert data into tables
for game in games_data:
    # Prepare data with default values for missing fields
    game_id = game.get('id')
    name = game.get('name', 'Unknown')  # Provide default value 'Unknown' if name is missing
    first_release_date = game.get('first_release_date', 0)  # Default to 0 if missing
    rating = game.get('rating', 0.0)  # Default to 0.0 if missing
    rating_count = game.get('rating_count', 0)  # Default to 0 if missing
    slug = game.get('slug', '')
    summary = game.get('summary', '')
    cover_url = game.get('cover', {}).get('url', '')  # Handle nested dictionaries

    # Insert game data into games table
    try:
        cursor.execute(
            'INSERT INTO games (id, name, first_release_date, rating, rating_count, slug, summary, cover_url) VALUES '
            '(?, ?, ?, ?, ?, ?, ?, ?)',
            (game_id, name, first_release_date, rating, rating_count, slug, summary, cover_url))
    except Exception as e:
        print(f"An error occurred while inserting game {game_id}: {e}")

    for genre_id in game.get('genres', []):
        try:
            cursor.execute('INSERT INTO game_genres (game_id, genre_id) VALUES (?, ?)', (game['id'], genre_id))
        except Exception as e:
            print(f"An error occurred while inserting into game_genres for game {game['id']}: {e}")

    # Insert connected data into respective tables
    for theme_id in game.get('themes', []):
        # Check if the entry already exists
        cursor.execute('SELECT * FROM game_themes WHERE game_id = ? AND theme_id = ?', (game['id'], theme_id))
        if cursor.fetchone() is None:  # If the entry does not exist, insert it
            try:
                cursor.execute('INSERT INTO game_themes (game_id, theme_id) VALUES (?, ?)', (game['id'], theme_id))
            except Exception as e:
                print(f"An error occurred while inserting into game_themes for game {game['id']}: {e}")

    for company_id in game.get('companies', []):
        cursor.execute('SELECT * FROM game_companies WHERE game_id = ? AND company_id = ?', (game_id, company_id))
        if cursor.fetchone() is None:
            try:
                cursor.execute('INSERT INTO game_companies (game_id, company_id) VALUES (?, ?)', (game_id, company_id))
            except Exception as e:
                print(f"An error occurred while inserting into game_companies for game {game_id}: {e}")

    # Insert data into game_modes with error handling and checking for existing entries
    for mode_id in game.get('modes', []):
        cursor.execute('SELECT * FROM game_modes WHERE game_id = ? AND mode_id = ?', (game_id, mode_id))
        if cursor.fetchone() is None:
            try:
                cursor.execute('INSERT INTO game_modes (game_id, mode_id) VALUES (?, ?)', (game_id, mode_id))
            except Exception as e:
                print(f"An error occurred while inserting into game_modes for game {game_id}: {e}")

    # Insert data into game_engines with error handling and checking for existing entries
    for engine_id in game.get('engines', []):
        cursor.execute('SELECT * FROM game_engines WHERE game_id = ? AND engine_id = ?', (game_id, engine_id))
        if cursor.fetchone() is None:
            try:
                cursor.execute('INSERT INTO game_engines (game_id, engine_id) VALUES (?, ?)', (game_id, engine_id))
            except Exception as e:
                print(f"An error occurred while inserting into game_engines for game {game_id}: {e}")

# Commit and close connection
conn.commit()
conn.close()

'''

'''
