import httpx
import os
from dotenv import load_dotenv

load_dotenv()

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
BASE_URL = "https://app.ticketmaster.com/discovery/v2"

async def search_events(location: str, keyword: str = None, radius: str = "25"):
    params = {
        "apikey": TICKETMASTER_API_KEY,
        "city": location,
        "radius": radius,
        "unit": "miles",
        "size": "20",
        "sort": "date,asc",
    }
    if keyword:
        params["keyword"] = keyword

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/events.json", params=params)
        response.raise_for_status()
        data = response.json()

    events = data.get("_embedded", {}).get("events", [])
    return [normalize_event(e) for e in events]


def normalize_event(e: dict) -> dict:
    venue = e.get("_embedded", {}).get("venues", [{}])[0]
    price_ranges = e.get("priceRanges", [])
    images = e.get("images", [])
    image = next((i["url"] for i in images if i.get("width", 0) > 500), None)

    price_str = None
    if price_ranges:
        p = price_ranges[0]
        min_p = p.get("min")
        max_p = p.get("max")
        if min_p and max_p:
            price_str = f"${min_p:.0f} – ${max_p:.0f}"
        elif min_p:
            price_str = f"From ${min_p:.0f}"

    dates = e.get("dates", {}).get("start", {})
    date_str = dates.get("localDate", "TBD")
    time_str = dates.get("localTime", "")
    if time_str:
        try:
            from datetime import datetime
            t = datetime.strptime(time_str, "%H:%M:%S")
            time_str = t.strftime("%I:%M %p").lstrip("0")
        except:
            pass

    return {
        "id": e.get("id"),
        "name": e.get("name"),
        "date": date_str,
        "time": time_str,
        "venue": venue.get("name", "Unknown Venue"),
        "address": f"{venue.get('city', {}).get('name', '')}, {venue.get('state', {}).get('stateCode', '')}",
        "category": e.get("classifications", [{}])[0].get("segment", {}).get("name", "Event"),
        "genre": e.get("classifications", [{}])[0].get("genre", {}).get("name", ""),
        "image": image,
        "price": price_str,
        "url": e.get("url"),
        "status": e.get("dates", {}).get("status", {}).get("code", ""),
    }