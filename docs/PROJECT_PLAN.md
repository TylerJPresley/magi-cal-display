# magi-cal-display - Project Plan

## Project Overview
A split-screen web application combining weather information with Google Calendar integration.

## Goals
- Display comprehensive weather data (current, hourly, radar) for configured location
- Integrate Google Calendar to show events from multiple calendars
- Split-screen layout with weather on top, calendar on bottom
- Seamless user experience with both data sources
- Reliable API integration for weather and calendar

## Technology Stack
- **Frontend**: Vue.js 3
- **Backend**: Python (FastAPI)
- **Weather API**: OpenWeatherMap One Call API 3.0 (free, 1000 calls/day)
- **Radar API**: RainViewer API (free)
- **Calendar**: Google Calendar iCal feeds (no API key needed)
- **Containerization**: Single container (Podman or Docker)
- **Deployment**: Raspberry Pi (ARM architecture)

## Project Phases

### Phase 1: Setup & Planning
- [x] Create project directory
- [x] Define technology stack
- [ ] Set up development environment
- [ ] Choose weather API provider
- [ ] Create single Dockerfile for combined app
- [ ] Configure FastAPI to serve static files

### Phase 2: Core Features - Weather
- [ ] Weather API integration (configurable location via lat/lon)
- [ ] Display current weather (temp, high/low, conditions)
- [ ] Hourly forecast display
- [ ] Weather radar integration
- [ ] Split-screen layout (top half)

### Phase 3: Core Features - Calendar
- [ ] iCal feed fetching and parsing
- [ ] ICS file format handling
- [ ] Display calendar events
- [ ] Multi-feed support
- [ ] Split-screen layout (bottom half)

### Phase 4: Enhanced Features
- [ ] Multi-day weather forecast
- [ ] Weather alerts for configured location
- [ ] Calendar event filtering
- [ ] Refresh/sync functionality
- [ ] Adjustable split-screen ratio

### Phase 5: Polish & Deploy
- [ ] Error handling
- [ ] Loading states
- [ ] Responsive design
- [ ] Testing
- [ ] Deployment

## Success Criteria
- Accurate weather data display
- Fast load times (< 2s)
- Mobile-responsive design
- Intuitive user experience
