from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
from icalendar import Calendar
from typing import List, Dict, Any
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="magi-cal-display API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")
HOME_ADDRESS = os.getenv("HOME_ADDRESS", "")
DESTINATION_ADDRESSES = os.getenv("DESTINATION_ADDRESSES", "").split(";") if os.getenv("DESTINATION_ADDRESSES") else []
ICAL_URLS = os.getenv("ICAL_URLS", "").split(",") if os.getenv("ICAL_URLS") else []
LOCATION_LAT = float(os.getenv("LOCATION_LAT", "35.0887"))
LOCATION_LON = float(os.getenv("LOCATION_LON", "-92.4421"))

# Hourly forecast indices (default: 1,2,3,4,5,6,8,12,20,28,38,47)
HOURLY_INDICES = os.getenv("HOURLY_INDICES", "1,2,3,4,5,6,8,12,20,28,38,47")

# Cache
weather_cache = {"data": None, "timestamp": None}
calendar_cache = {"data": None, "timestamp": None}
i40_cache = {"data": None, "timestamp": None}
CACHE_DURATION = int(os.getenv("REFRESH_INTERVAL", "120"))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    destinations = []
    for dest in DESTINATION_ADDRESSES:
        if "|" in dest:
            name, address = dest.split("|", 1)
            destinations.append({"name": name.strip(), "address": address.strip()})
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "config": {
            "has_weather_key": bool(OPENWEATHER_API_KEY),
            "has_tomtom_key": bool(TOMTOM_API_KEY),
            "tomtom_api_key": TOMTOM_API_KEY,
            "openweather_api_key": OPENWEATHER_API_KEY,
            "calendar_feeds": len(ICAL_URLS),
            "location": {"lat": LOCATION_LAT, "lon": LOCATION_LON},
            "refresh_interval": CACHE_DURATION,
            "hourly_indices": HOURLY_INDICES,
            "home_address": HOME_ADDRESS,
            "destinations": destinations
        }
    }


def geocode_address(address: str) -> dict:
    """Geocode an address using TomTom Search API"""
    try:
        url = "https://api.tomtom.com/search/2/geocode/" + address + ".json"
        params = {
            "key": TOMTOM_API_KEY,
            "limit": 1
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("results") and len(data["results"]) > 0:
                position = data["results"][0]["position"]
                return {"lat": position["lat"], "lon": position["lon"]}
        
        return None
    except Exception as e:
        logger.error(f"Geocoding error for {address}: {e}")
        return None


@app.get("/api/drive-times")
async def get_drive_times():
    """Get drive times from home to destinations using TomTom Routing API"""
    if not TOMTOM_API_KEY or not HOME_ADDRESS or not DESTINATION_ADDRESSES:
        return {"drive_times": []}
    
    try:
        # Geocode home address
        home_coords = geocode_address(HOME_ADDRESS)
        if not home_coords:
            logger.error(f"Failed to geocode home address: {HOME_ADDRESS}")
            return {"drive_times": []}
        
        drive_times = []
        
        for dest in DESTINATION_ADDRESSES:
            if "|" not in dest:
                continue
            
            name, address = dest.split("|", 1)
            name = name.strip()
            address = address.strip()
            
            # Geocode destination address
            dest_coords = geocode_address(address)
            if not dest_coords:
                logger.error(f"Failed to geocode destination: {address}")
                continue
            
            # Use TomTom Routing API with coordinates
            url = f"https://api.tomtom.com/routing/1/calculateRoute/{home_coords['lat']},{home_coords['lon']}:{dest_coords['lat']},{dest_coords['lon']}/json"
            params = {
                "key": TOMTOM_API_KEY,
                "traffic": "true",
                "travelMode": "car"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("routes") and len(data["routes"]) > 0:
                    route = data["routes"][0]
                    summary = route.get("summary", {})

                    travel_time_seconds = summary.get("travelTimeInSeconds", 0)
                    traffic_delay_seconds = summary.get("trafficDelayInSeconds", 0)
                    distance_meters = summary.get("lengthInMeters", 0)

                    # Extract route polyline from legs
                    polyline = []
                    for leg in route.get("legs", []):
                        for point in leg.get("points", []):
                            polyline.append([point["latitude"], point["longitude"]])

                    drive_times.append({
                        "name": name,
                        "address": address,
                        "travel_time_minutes": round(travel_time_seconds / 60),
                        "traffic_delay_minutes": round(traffic_delay_seconds / 60),
                        "distance_miles": round(distance_meters / 1609.34, 1),
                        "lat": dest_coords["lat"],
                        "lon": dest_coords["lon"],
                        "polyline": polyline
                    })
        
        return {
            "drive_times": drive_times,
            "home_coords": home_coords
        }
    
    except Exception as e:
        logger.error(f"Error fetching drive times: {e}")
        return {"drive_times": [], "home_coords": None}

@app.get("/api/i40-status")
async def get_i40_status():
    """Check for traffic delays on I-40 between Conway and Little Rock"""

    # Check cache
    if i40_cache["data"] is not None and i40_cache["timestamp"]:
        age = (datetime.now() - i40_cache["timestamp"]).total_seconds()
        if age < CACHE_DURATION:
            return i40_cache["data"]

    if not TOMTOM_API_KEY:
        return {"has_delay": False, "delay_minutes": 0, "reason": None}

    # Conway, AR → Little Rock, AR (I-40 corridor)
    conway_lat, conway_lon = 35.0887, -92.4421
    lr_lat, lr_lon = 34.7465, -92.2896

    try:
        # Get current route with traffic
        route_url = f"https://api.tomtom.com/routing/1/calculateRoute/{conway_lat},{conway_lon}:{lr_lat},{lr_lon}/json"
        route_response = requests.get(route_url, params={
            "key": TOMTOM_API_KEY,
            "traffic": "true",
            "travelMode": "car"
        }, timeout=10)

        delay_minutes = 0
        if route_response.status_code == 200:
            route_data = route_response.json()
            if route_data.get("routes"):
                summary = route_data["routes"][0]["summary"]
                delay_minutes = round(summary.get("trafficDelayInSeconds", 0) / 60)

        # If there's a delay, look for the reason on I-40
        reason = None
        if delay_minutes > 0:
            incident_response = requests.get(
                "https://api.tomtom.com/traffic/services/5/incidentDetails",
                params={
                    "key": TOMTOM_API_KEY,
                    "bbox": "-92.50,34.68,-92.22,35.15",  # I-40 Conway↔Little Rock corridor
                    "fields": "{incidents{properties{iconCategory,magnitudeOfDelay,events{description},from,roadNumbers}}}",
                    "language": "en-US",
                    "timeValidityFilter": "present"
                },
                timeout=10
            )

            if incident_response.status_code == 200:
                category_map = {
                    1: "Accident", 2: "Fog", 3: "Dangerous Conditions",
                    4: "Rain", 5: "Ice", 6: "Traffic Jam", 7: "Lane Closed",
                    8: "Road Closed", 9: "Road Works", 10: "High Winds",
                    11: "Flooding", 14: "Disabled Vehicle"
                }
                best = None
                for incident in incident_response.json().get("incidents", []):
                    props = incident.get("properties", {})
                    if props.get("magnitudeOfDelay", 0) < 1:
                        continue
                    road_numbers = props.get("roadNumbers", [])
                    if not any("40" in str(r) for r in road_numbers):
                        continue
                    if best is None or props.get("magnitudeOfDelay", 0) > best.get("magnitudeOfDelay", 0):
                        best = props

                if best:
                    events = best.get("events", [])
                    description = events[0].get("description", "") if events else ""
                    category = category_map.get(best.get("iconCategory", 0), "Incident")
                    reason = description if description else category

        result = {"has_delay": delay_minutes > 0, "delay_minutes": delay_minutes, "reason": reason}
        i40_cache["data"] = result
        i40_cache["timestamp"] = datetime.now()
        logger.info(f"I-40 status: delay={delay_minutes}min reason={reason}")
        return result

    except Exception as e:
        logger.error(f"Error checking I-40 status: {e}")
        return {"has_delay": False, "delay_minutes": 0, "reason": None}


@app.get("/api/weather")
async def get_weather():
    """Get weather data from OpenWeatherMap One Call API 3.0"""
    
    # Check cache
    if weather_cache["data"] and weather_cache["timestamp"]:
        age = (datetime.now() - weather_cache["timestamp"]).total_seconds()
        if age < CACHE_DURATION:
            logger.info(f"Returning cached weather data (age: {age}s)")
            return weather_cache["data"]
    
    if not OPENWEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenWeather API key not configured")
    
    try:
        # One Call API 3.0
        url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            "lat": LOCATION_LAT,
            "lon": LOCATION_LON,
            "appid": OPENWEATHER_API_KEY,
            "units": "imperial",
            "exclude": "minutely"
        }
        
        logger.info(f"Fetching weather data for {LOCATION_LAT}, {LOCATION_LON}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Fetch air quality data
        air_url = "http://api.openweathermap.org/data/2.5/air_pollution"
        air_params = {
            "lat": LOCATION_LAT,
            "lon": LOCATION_LON,
            "appid": OPENWEATHER_API_KEY
        }
        air_response = requests.get(air_url, params=air_params, timeout=10)
        air_response.raise_for_status()
        air_data = air_response.json()
        
        # Add air quality to weather data
        if air_data.get("list") and len(air_data["list"]) > 0:
            data["air_quality"] = air_data["list"][0]
        
        # Update cache
        weather_cache["data"] = data
        weather_cache["timestamp"] = datetime.now()
        
        logger.info("Weather data fetched successfully")
        return data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather data: {str(e)}")


@app.get("/api/calendar")
async def get_calendar_events():
    """Get calendar events from iCal feeds"""
    
    # Check cache
    if calendar_cache["data"] and calendar_cache["timestamp"]:
        age = (datetime.now() - calendar_cache["timestamp"]).total_seconds()
        if age < CACHE_DURATION:
            logger.info(f"Returning cached calendar data (age: {age}s)")
            return calendar_cache["data"]
    
    if not ICAL_URLS or not ICAL_URLS[0]:
        raise HTTPException(status_code=500, detail="No calendar URLs configured")
    
    all_events = []
    
    for idx, ical_url in enumerate(ICAL_URLS):
        if not ical_url.strip():
            continue
            
        try:
            logger.info(f"Fetching calendar feed {idx + 1}/{len(ICAL_URLS)}")
            response = requests.get(ical_url.strip(), timeout=10)
            response.raise_for_status()
            
            # Parse iCal data
            cal = Calendar.from_ical(response.content)
            
            # Extract events
            for component in cal.walk():
                if component.name == "VEVENT":
                    start_dt = component.get("dtstart").dt if component.get("dtstart") else None
                    end_dt = component.get("dtend").dt if component.get("dtend") else None
                    
                    # Detect all-day events (date objects without time)
                    is_all_day = start_dt and not isinstance(start_dt, datetime)
                    
                    event = {
                        "summary": str(component.get("summary", "No Title")),
                        "start": start_dt,
                        "end": end_dt,
                        "description": str(component.get("description", "")),
                        "location": str(component.get("location", "")),
                        "calendar_index": idx,
                        "all_day": is_all_day
                    }
                    
                    # Convert datetime to ISO string
                    if event["start"]:
                        if isinstance(event["start"], datetime):
                            event["start"] = event["start"].isoformat()
                        else:
                            event["start"] = datetime.combine(event["start"], datetime.min.time()).isoformat()
                    
                    if event["end"]:
                        if isinstance(event["end"], datetime):
                            event["end"] = event["end"].isoformat()
                        else:
                            event["end"] = datetime.combine(event["end"], datetime.min.time()).isoformat()
                    
                    all_events.append(event)
                    
        except Exception as e:
            logger.error(f"Error fetching calendar feed {idx + 1}: {e}")
            continue
    
    # Sort events by start time
    all_events.sort(key=lambda x: x["start"] if x["start"] else "")
    
    # Filter to 1 month before and 1 month after to catch multi-day events
    now = datetime.now()
    start_range = now - timedelta(days=30)
    end_range = now + timedelta(days=35)  # 5 days + 30 days buffer
    
    filtered_events = []
    for e in all_events:
        if e["start"]:
            try:
                event_start = datetime.fromisoformat(e["start"])
                # Make timezone-naive for comparison
                if event_start.tzinfo:
                    event_start = event_start.replace(tzinfo=None)
                
                # Check if event starts or ends within our range
                event_end = None
                if e["end"]:
                    event_end = datetime.fromisoformat(e["end"])
                    if event_end.tzinfo:
                        event_end = event_end.replace(tzinfo=None)
                
                # Include event if it starts before end_range and ends after start_range
                if event_end:
                    if event_start <= end_range and event_end >= start_range:
                        filtered_events.append(e)
                else:
                    if event_start >= start_range and event_start <= end_range:
                        filtered_events.append(e)
            except:
                continue
    
    result = {
        "events": filtered_events,
        "count": len(filtered_events),
        "feeds_processed": len([u for u in ICAL_URLS if u.strip()])
    }
    
    # Update cache
    calendar_cache["data"] = result
    calendar_cache["timestamp"] = datetime.now()
    
    logger.info(f"Calendar data fetched successfully: {len(filtered_events)} events")
    return result


# Serve static files (Vue.js frontend)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve the Vue.js frontend"""
        # API routes are handled above
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404)
        
        # Serve index.html for all other routes with no-cache headers
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(
                index_path,
                headers={
                    "Cache-Control": "no-cache, no-store, must-revalidate",
                    "Pragma": "no-cache",
                    "Expires": "0"
                }
            )
        return {"message": "Frontend not built yet. Run: cd frontend && npm run build"}
else:
    @app.get("/")
    async def root():
        """Serve the frontend"""
        return {
            "message": "magi-cal-display API",
            "version": "1.0.0",
            "endpoints": {
                "health": "/api/health",
                "weather": "/api/weather",
                "calendar": "/api/calendar"
            },
            "note": "Frontend not built yet. Run: cd frontend && npm run build"
        }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
