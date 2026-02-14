import requests

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Error fetching IP"

def get_utc_time():
    try:
        data = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Etc/UTC").json()
        return data.get('dateTime', 'Error')
    except:
        return "Error fetching time"

def get_weather(lat, lon):
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,precipitation",
            "timezone": "auto"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        current = data["current"]
        temp = current["temperature_2m"]
        feels_like = current["apparent_temperature"]
        humidity = current["relative_humidity_2m"]
        wind = current["wind_speed_10m"]
        precip = current["precipitation"]
        code = current["weather_code"]

        weather_codes = {
            0: "Clear sky ☀️",
            1: "Mainly clear 🌤️",
            2: "Partly cloudy ⛅",
            3: "Overcast ☁️",
            45: "Fog 🌫️",
            51: "Light drizzle 🌧️",
            61: "Light rain 🌧️",
            63: "Moderate rain 🌧️",
            71: "Light snow ❄️",
            80: "Rain showers 🌦️",
            95: "Thunderstorm ⛈️",
        }
        condition = weather_codes.get(code, f"Unknown (code {code})")

        return (f"{temp}°C (feels like {feels_like}°C), {condition}\n"
                f"Humidity: {humidity}%, Wind: {wind} km/h, Precipitation: {precip} mm")

    except requests.exceptions.RequestException as e:
        return f"Network error: {e}"
    except Exception as e:
        return f"Error: {e} (check city name or try again)"

# Main part
print("Hello from Python! 🌟")
print("Your public IP address is:", get_public_ip())
print("Current UTC time:", get_utc_time())

# Ask for city
city = input("\nEnter city name (e.g. Tirana, New York, London): ").strip()

if not city:
    print("No city entered. Using default (Tirana).")
    lat, lon = 41.33, 19.82
else:
    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": city,
            "count": 1,           # get the best/first match
            "language": "en",
            "format": "json"
        }
        geo_response = requests.get(geo_url, params=geo_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if "results" in geo_data and geo_data["results"]:
            result = geo_data["results"][0]
            lat = result["latitude"]
            lon = result["longitude"]
            found_name = result.get("name", city)
            country = result.get("country", "")
            print(f"Found: {found_name}, {country}")
        else:
            print(f"City '{city}' not found. Using default (Tirana).")
            lat, lon = 41.33, 19.82
    except Exception as e:
        print(f"Error looking up city: {e}. Using default (Tirana).")
        lat, lon = 41.33, 19.82

print(f"\nCurrent weather in {city.capitalize() if city else 'Tirana'}:")
print(get_weather(lat, lon))
