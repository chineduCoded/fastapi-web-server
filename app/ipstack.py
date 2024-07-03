import requests
from config import settings

def ip_stack(client_ip: str):
    ipstack_url = f"http://api.ipstack.com/{client_ip}?access_key={settings.ipstack_api_key}"
    response = requests.get(ipstack_url)
    response.raise_for_status()

    return response.json()