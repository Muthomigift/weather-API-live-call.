"""
Travel Weather Tool
--------------------
shows weather and country information for any city.

usage 
    python day3_travel_info.py
    
requirements:
    pip install requests, python dotenv
    OPEN_WEATHER_API_KEY in .env file
"""
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def get_country_info(country_code):
    info_url = f"https://api.worldbank.org/v2/country/{country_code}?format=json"
    pop_url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/SP.POP.TOTL?format=json&mrv=1"

    info_response = requests.get(info_url)
    pop_response = requests.get(pop_url)

    if info_response.status_code != 200 or pop_response.status_code != 200:
        return None

    try:
        country = info_response.json()[1][0]
        population = pop_response.json()[1][0]["value"] or 0
        return {
            "region": country["region"]["value"],
            "capital": country["capitalCity"],
            "population": population,
        }
    except (IndexError, KeyError, TypeError):
        return None

def save_to_file (data,filenames):
    with open (filenames, "w") as f:
        json.dump(data, f, indent =2)
    print(f"Data saved to {filenames}") 


def run_tool():
    print("Travel Weather Tool")
    print("-------------------")
    city = input("Enter a city name: ").strip()

    if not city:
        print("No city entered. Exiting.")
        return

    print(f"\nFetching data for {city}...")

    weather_data = get_weather(city)

    if not weather_data:
        print(f"Could not find weather data for '{city}'. Check the city name and try again.")
        return

    country_code = weather_data["sys"]["country"]
    country_data = get_country_info(country_code)

    print(f"\n=== {city.title()}, {country_code} ===")
    print(f"Temperature : {weather_data['main']['temp']}C")
    print(f"Condition   : {weather_data['weather'][0]['description'].title()}")
    print(f"Humidity    : {weather_data['main']['humidity']}%")
    print(f"Wind        : {weather_data['wind']['speed']} m/s")

    if country_data:
        population = country_data.get("population", 0)
        region = country_data.get("region", "Unknown")
        currencies = ", ".join(country_data.get("currencies", {}).keys())
        print(f"\n=== Country Info ===")
        print(f"Region      : {region}")
        print(f"Population  : {population:,}")
        print(f"Currency    : {currencies}")

    if weather_data:
        save_to_file(weather_data, f"{city.lower()}_weather.json")
run_tool()