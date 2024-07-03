import requests
from config import settings

def get_location_and_temperature(client_ip: str):
    """
    Get location and temperature of client IP.

    args:
        client_ip: str -> client IP address
    
    return:
        location and temperature.
    """
    try:
        ipstack_url = f"http://api.ipstack.com/{client_ip}?access_key={settings.ipstack_api_key}"
        response = requests.get(ipstack_url)
        response.raise_for_status()
        data = response.json()
        
        city = data["region_name"]
        latitude = data["latitude"]
        longitude = data["longitude"]

        if latitude and longitude:
            openweathermap_url = (
                f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={settings.openweathermap_api_key}&units=metric"
            )
            response = requests.get(openweathermap_url)
            response.raise_for_status()
            data = response.json()
            temperature = data["main"]["temp"]
        else:
            temperature = "Unknown"
        
        return city, temperature
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None, "Unknown"
    except KeyError as e:
        print(f"Key error: {e}")
        return None, "Unknown"
