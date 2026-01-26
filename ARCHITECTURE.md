# magi-cal-display - Architecture

## System Architecture

### Architecture Pattern
Single Page Application (SPA) with Vue.js frontend and Python FastAPI REST API backend

## Component Structure

### Frontend Components
```
App
├── CombinedView (main component)
│   ├── Weather Alerts (full-width at top)
│   ├── Main Content (responsive layout)
│   │   ├── Weather Column
│   │   │   ├── Current Overview
│   │   │   │   ├── Temperature & Conditions
│   │   │   │   ├── Wind Compass
│   │   │   │   ├── High/Low
│   │   │   │   └── Feels Like
│   │   │   ├── Air Quality (AQI with pollutant breakdown)
│   │   │   ├── Hourly Forecast (12 hours, indices: [1,2,3,4,5,6,8,12,20,28,38,47])
│   │   │   └── Weather Radar (live precipitation map)
│   │   │
│   │   └── Calendar Column
│   │       └── Next 6 Days (Today + 5)
│   │           ├── Day Header (date, weather icon, temp range)
│   │           └── Events (time, title, location, calendar color)
│   │
│   └── Responsive Layout
│       ├── Landscape: Side-by-side (weather left, calendar right)
│       └── Portrait: Stacked (weather top, calendar bottom)
```

### Backend/API Layer
- Weather API integration service (OpenWeatherMap One Call API 3.0)
- Air Quality API integration (OpenWeatherMap Air Pollution API)
- Radar API integration (RainViewer)
- Google Calendar iCal feed parser
- ICS file parsing and event extraction
- Multi-day event handling
- Data transformation/normalization
- Response caching and error handling

## Data Flow

### Weather Data Flow
1. Backend reads location from environment variables (LOCATION_LAT, LOCATION_LON)
2. Frontend requests weather data from backend API
3. Backend calls OpenWeatherMap One Call API 3.0 with lat/lon coordinates
4. Backend calls OpenWeatherMap Air Pollution API with same lat/lon
5. Backend calls RainViewer API for radar imagery centered on lat/lon
6. Weather data (current, hourly, daily, alerts, AQI, radar) is processed
7. Response sent to frontend with all weather information
8. Weather section updates with current conditions, forecasts, alerts, AQI, and radar
9. Auto-refresh every 2 minutes

### Calendar Data Flow
1. User provides iCal feed URLs via environment variable (secret links from Google Calendar)
2. Backend fetches ICS files from URLs on each refresh
3. Parse ICS format to extract events (VEVENT components)
4. Handle multi-day events (DTSTART/DTEND spanning multiple days)
5. Filter events by date range (past 7 days to future 30 days)
6. Format events with time, title, and calendar color
7. Calendar section displays events grouped by date
8. Auto-refresh every 2 minutes to sync new events

## API Integration
- **Primary Weather API**: OpenWeatherMap One Call API 3.0
  - Endpoint: Current weather, minute forecast (1hr), hourly (48hrs), daily (8 days), weather alerts
  - Location: Determined by LOCATION_LAT and LOCATION_LON environment variables (required)
  - Rate limit: 1000 calls per day (free tier)
  - Refresh interval: 2 minutes (120 seconds) = 720 calls/day
  - Features: Temperature, humidity, wind, precipitation, UV index, weather alerts, feels like
- **Air Quality API**: OpenWeatherMap Air Pollution API
  - Endpoint: Current air pollution data
  - Provides: AQI (Air Quality Index) and pollutant concentrations
  - Pollutants: PM2.5, PM10, O₃ (Ozone), NO₂ (Nitrogen Dioxide), SO₂, CO
  - Location: Same lat/lon from environment variables as weather API
  - Same refresh interval as weather data
- **Radar API**: RainViewer API (free, no key required)
  - Provides: Past 2 hours + 30 min forecast radar tiles
  - Map tile overlay for precipitation visualization
  - Auto-refresh every 10 minutes
  - Animated radar loop showing precipitation movement
- **Google Calendar**: iCal feed URLs (no OAuth required)
  - Comma-separated list of iCal URLs via environment variable
  - Parse ICS format for events (VEVENT components)
  - Multi-day event support (DTSTART/DTEND)
  - Refresh interval: 2 minutes (120 seconds)
  - Configuration: `ICAL_URLS="url1,url2,url3"` in env file
- **Rate Limiting**: Respects API rate limits, uses appropriate refresh intervals

## State Management
- **Vue Composition API**: Local component state with reactive refs
- **Auto-refresh**: Configurable via REFRESH_INTERVAL environment variable (default: 120 seconds)
  - Weather and calendar data refresh based on configured interval
  - Radar updates every 10 minutes
  - Refresh interval fetched from backend /api/health endpoint on mount
- **No Global State**: Simple architecture without Pinia/Vuex
- **Data Fetching**: Direct API calls from CombinedView component to backend endpoints

## Error Handling Strategy
- Network errors: Display error message, retry on next refresh cycle
- Invalid API key: Show configuration error
- API rate limits: Continue using last successful data
- Missing calendar URLs: Show empty calendar section
- Timeout: Fallback to last known data, retry on next cycle

## Deployment Architecture
- **Containerization**: Single container (Podman or Docker), multi-stage build
- **Container Structure**: 
  - Stage 1: Node.js to build Vue.js frontend
  - Stage 2: Python with FastAPI serving both API and static Vue.js build
- **Web Server**: FastAPI with static file serving (no separate Nginx)
- **Runtime**: Python 3.11+ with Uvicorn ASGI server
- **Networking**: Single container, exposed port 3000
- **No Volumes**: Stateless container, no persistent storage needed
- **Environment Variables**: 
  - `OPENWEATHER_API_KEY` - OpenWeatherMap API key (required)
  - `ICAL_URLS` - Comma-separated list of iCal feed URLs (required)
  - `LOCATION_LAT` - Latitude (required)
  - `LOCATION_LON` - Longitude (required)
  - `REFRESH_INTERVAL` - Refresh interval in seconds (default: 120)
  - `HOURLY_INDICES` - Comma-separated hour indices 0-47 to display (default: 1,2,3,4,5,6,8,12,20,28,38,47)
  - `PORT` - Server port (default: 3000)
- **Target Platform**: Platform-agnostic (Linux, macOS, Windows with container runtime)
- **Auto-restart**: Container configured with `--restart always` flag
