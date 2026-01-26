# magi-cal-display - Deployment Summary

## ✅ Successfully Deployed!

**Container ID:** Running
**Port:** http://127.0.0.1:3000
**Status:** Healthy

## What's Running

- **Weather Data:** OpenWeatherMap One Call API 3.0
- **Calendar:** 2 Google Calendar iCal feeds
- **Auto-refresh:** Every 2 minutes
- **Container:** Single container (Podman or Docker) with Vue.js + FastAPI

## Quick Commands

### View the app
```bash
# Open in browser
xdg-open http://127.0.0.1:3000
```

### Check status
```bash
# Podman
podman ps | grep magi-cal-display
podman logs -f magi-cal-display

# Docker
docker ps | grep magi-cal-display
docker logs -f magi-cal-display
```

### Stop/Start
```bash
# Podman
podman stop magi-cal-display
podman start magi-cal-display

# Docker
docker stop magi-cal-display
docker start magi-cal-display
```

### Update configuration
```bash
# Edit the env file
vim ~/Projects/magi-cal-display/magi-cal-display.env.list

# Restart to apply changes (Podman)
podman restart magi-cal-display

# Or with Docker
docker restart magi-cal-display
```

### Rebuild after code changes
```bash
cd ~/Projects/magi-cal-display
./build.sh

# Podman
podman run -d --name magi-cal-display --replace -p 127.0.0.1:3000:3000 --env-file magi-cal-display.env.list --restart always magi-cal-display:latest

# Docker
docker stop magi-cal-display && docker rm magi-cal-display
docker run -d --name magi-cal-display -p 127.0.0.1:3000:3000 --env-file magi-cal-display.env.list --restart always magi-cal-display:latest
```

## API Endpoints

- `http://127.0.0.1:3000/` - Main app
- `http://127.0.0.1:3000/api/health` - Health check
- `http://127.0.0.1:3000/api/weather` - Weather data
- `http://127.0.0.1:3000/api/calendar` - Calendar events

## For Raspberry Pi Deployment

1. Copy the project to your Pi:
   ```bash
   scp -r ~/Projects/magi-cal-display pi@raspberrypi:~/
   ```

2. On the Pi, build and run:
   ```bash
   cd ~/magi-cal-display
   ./build.sh
   podman run -d --name magi-cal-display --replace -p 3000:3000 --env-file magi-cal-display.env.list --restart always magi-cal-display:latest
   ```

3. Access from any device on your network:
   ```
   http://raspberrypi.local:3000
   ```

## Features

✅ Current weather with temperature, conditions, humidity, wind
✅ 12-hour hourly forecast
✅ 8-day daily forecast  
✅ Weather alerts
✅ Google Calendar events from multiple calendars
✅ Color-coded calendar events
✅ Auto-refresh every 2 minutes
✅ Dark theme optimized for displays
✅ Single container deployment
✅ Low resource usage for Raspberry Pi

## Configuration

All settings in `magi-cal-display.env.list`:
- `OPENWEATHER_API_KEY` - Your API key
- `ICAL_URLS` - Comma-separated calendar URLs
- `LOCATION_LAT` / `LOCATION_LON` - Location coordinates
- `REFRESH_INTERVAL` - Refresh time in seconds (default: 120)
- `PORT` - Server port (default: 3000)

Enjoy your magi-cal-display! 🌤️📅
