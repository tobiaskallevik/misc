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


def fetch_companies(auth_token, involved_companies_id):
    url = "https://api.igdb.com/v4/involved_companies"
    headers = {
        "Accept": "application/json",
        "Client-ID": client_id,
        "Authorization": "Bearer " + auth_token,
        "Content-Type": "text/plain"
    }
    data = ('fields company.name, company.slug, company.description, company.logo, '
            'company.start_date;'
            'limit 500;'
            'sort id asc;'
            'where id >' + str(involved_companies_id) + ';')
    response = requests.post(url, headers=headers, data=data)

    # If the response is 401, get a new auth token and recursively call the function
    if response.status_code == 401:
        auth_token = get_auth_token()
        return fetch_igdb_games(auth_token, involved_companies_id)

    return response.json()


# Create a json file
def create_json(file_name):
    with open(file_name, "w") as file:
        file.write("[]")


# Write to the json file
def write_to_json(data, file_name):
    with open(file_name, "r") as file:
        games = json.load(file)
        games.extend(data)  # Extend the list with the new data
    with open(file_name, "w") as file:
        json.dump(games, file, indent=4)


# Main function
def initiate_games():
    file_name = "games2.json"
    create_json(file_name)
    auth_token = get_auth_token()
    game_id = 160499

    while True:
        response = fetch_igdb_games(auth_token, game_id)
        if len(response) == 0:
            print("Got all games")
            break

        write_to_json(response, file_name)
        print("Got games from id " + str(game_id), "to " + str(game_id + 500))
        game_id += 500


def initiate_companies():
    file_name = "companies.json"
    create_json(file_name)
    auth_token = get_auth_token()
    involved_companies_id = 0
    companies = []

    while True:
        response = fetch_companies(auth_token, involved_companies_id)
        if len(response) == 0:
            print("Got all companies")
            break

        for item in response:
            company_id = item.get("id", "N/A")
            company = item.get("company", {})
            name = company.get("name", "N/A")
            slug = company.get("slug", "N/A")
            description = company.get("description", "N/A")
            logo = company.get("logo", "N/A")
            start_date = company.get("start_date", "N/A")

            cut_down_response = {
                "id": company_id,
                "name": name,
                "slug": slug,
                "description": description,
                "logo": logo,
                "start_date": start_date
            }

            involved_companies_id = company_id

            companies.append(cut_down_response)

        print("Got companies to id " + str(involved_companies_id))
        involved_companies_id += 1

    write_to_json(companies, file_name)


if __name__ == "__main__":
    # initiate_games()
    initiate_companies()
