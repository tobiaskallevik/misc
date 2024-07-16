import math
import os
import random
import sqlite3
import json
import time

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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(base_url, params=query_params, headers=headers)

    # Print the final URL (for debugging)
    print("Final URL:", response.url)

    # Error handling
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        return None

    return response.json()


def create_json():
    with open("gamesImages.json", "w") as file:
        file.write("[]")


def write_to_json(game_id, game_name, image_url):
    with open("gamesImages.json", "r") as file:
        games = json.load(file)
        games.append({"game_id": game_id, "game_name": game_name, "image_url": image_url})
    with open("gamesImages.json", "w") as file:
        json.dump(games, file, indent=4)


# Gets the game name and game id from the database.
# Then gets the image url from the Giant Bomb API.
# Finally, writes the game id, name and image url to a JSON file.
def main():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    last_game_id = 0

    # Get the id last game from the last element in the gamesImages.json file
    try:
        with open("gamesImages.json", "r") as file:
            games = json.load(file)
            if games:  # Check if the list is not empty
                last_game_id = games[-1]["game_id"]
            else:
                print("gamesImages.json is empty. Starting from the beginning.")
    except FileNotFoundError:
        print("gamesImages.json not found. Creating a new file.")
        create_json()

    for row in cursor.execute("SELECT id, name FROM games WHERE id > ?", (last_game_id,)):
        game_id, game_name = row
        response = get_game_info(game_name)

        if response is not None:
            image_url = response["results"][0]["image"]["medium_url"]
            write_to_json(game_id, game_name, image_url)
            print("Got image for", game_name)

        else:
            print("No image found for", game_name)

        time.sleep(round(random.uniform(2, 4), 3))

    conn.close()


if __name__ == "__main__":
    main()
