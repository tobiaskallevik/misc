import json
import time
import os
import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")


# Get the auth token
def get_auth_token():
    url = "https://id.twitch.tv/oauth2/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, data=payload)
    print("Auth token is" + response.json()["access_token"])
    return response.json()["access_token"]


# Fetch games
def fetch_igdb_games(auth_token, game_id):
    url = "https://api.igdb.com/v4/games"
    headers = {
        "Accept": "application/json",
        "Client-ID": client_id,
        "Authorization": "Bearer " + auth_token,
        "Content-Type": "text/plain"
    }
    data = ('fields name, rating, rating_count, summary, involved_companies, first_release_date, slug, themes, '
            'player_perspectives, game_engines, cover.url, genres, game_modes, version_title, version_parent;'
            'limit 500;'
            'sort id asc;'
            'where rating != null & rating_count != null & cover != null;'
            'where id >' + str(game_id) + ';')
    response = requests.post(url, headers=headers, data=data)

    # If the response is 401, get a new auth token and recursively call the function
    if response.status_code == 401:
        auth_token = get_auth_token()
        return fetch_igdb_games(auth_token, game_id)

    return response.json()


# Create a json file
def create_json():
    with open("games2.json", "w") as file:
        file.write("[]")


# Write to the json file
def write_to_json(data):
    with open("games2.json", "r") as file:
        games = json.load(file)
        games.extend(data)  # Extend the list with the new data
    with open("games2.json", "w") as file:
        json.dump(games, file, indent=4)  # Optional: add indent for better readability


# Main function
def main():
    create_json()
    auth_token = get_auth_token()
    game_id = 160499

    while True:
        response = fetch_igdb_games(auth_token, game_id)
        if len(response) == 0:
            print("Got all games")
            break

        write_to_json(response)
        print("Got games from id " + str(game_id), "to " + str(game_id + 500))
        game_id += 500


if __name__ == "__main__":
    main()
