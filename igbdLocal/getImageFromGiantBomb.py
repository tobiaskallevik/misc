import os
import sqlite3
import json
import requests
from dotenv import load_dotenv

load_dotenv()


def get_game_info(game_name):
    api_key = os.getenv("GIANT_BOMB_API_KEY")
    base_url = "https://www.giantbomb.com/api/search/"
    query_params = {
        "api_key": api_key,
        "format": "json",
        "query": f'"{game_name}"',
        "resources": "game",
        "limit": 1,
        "field_list": "image"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(base_url, params=query_params, headers=headers)

    # Print the final URL (for debugging)
    print("Final URL:", response.url)

    # Error handling
    try:
        response.raise_for_status()

    # Extraxt the medium image url
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        return None

    return response.json()


def create_json():
    with open("gamesImages.json", "w") as file:
        file.write("[]")


def write_to_json(id, image_url):
    with open("gamesImages.json", "r") as file:
        games = json.load(file)
        games.append({"id": id, "image_url": image_url})
    with open("gamesImages.json", "w") as file:
        json.dump(games, file, indent=4)


# Gets the game name and game id from the database
def main():
    conn = sqlite3.connect('games.db')  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object

    for row in cursor.execute("SELECT id, name FROM games"):
        game_id, game_name = row
        print(f"Getting image for {game_name}")


if __name__ == "__main__":
    main()
