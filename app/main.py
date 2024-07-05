import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.utils.location_temperature import get_location_and_temperature


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/", status_code=200)
async def read_root():
    """
    Check health status of the API
    """
    return {"status": "Running!"}


@app.get("/api/hello", status_code=200)
async def greetings(request: Request, visitor_name: str = "Guest"):
    """Greeting visitors"""
    client_ip = requests.get("https://httpbin.org/ip").json()['origin']

    city, temperature = get_location_and_temperature(client_ip)
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"

    return JSONResponse({
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    })