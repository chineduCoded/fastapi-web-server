from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.utils.location_temperature import get_location_and_temperature
from app.ipstack import ip_stack


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
    client_ip = request.client.host

    if client_ip == "127.0.0.1":
        # A fallback IP address for testing locally. Example: Google Public DNS IP address
        client_ip = "8.8.8.8"
    city, temperature = get_location_and_temperature(client_ip)
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"

    return JSONResponse({
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    })