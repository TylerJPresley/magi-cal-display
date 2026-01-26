# magi-cal-display - Requirements

## Application Overview
Split-screen web application displaying weather information (top half) and Google Calendar integration (bottom half).

## Functional Requirements

### Weather Section (Top Half) - Must Have
1. Display current temperature for configured location
2. Show high/low temperatures
3. Display current weather conditions
4. Hourly forecast view
5. Weather radar display
6. Basic weather metrics (humidity, wind speed, precipitation)
7. Weather icons/visuals
8. Auto-refresh weather data every 2 minutes (720 API calls per 24 hours)

### Calendar Section (Bottom Half) - Must Have
1. Google Calendar iCal feed integration
2. Display events from multiple iCal feed URLs
3. Show multiple calendar sources simultaneously
4. Event details (time, title, description, location)
5. Current day/week/month view
6. Auto-refresh calendar data every 2 minutes
7. Configuration UI for adding/removing iCal feed URLs

### Should Have
1. Multi-day weather forecast (5-7 days)
2. Calendar event filtering by calendar source
3. Refresh/sync functionality for both sections
4. Responsive split-screen layout
5. Weather alerts for configured location

### Nice to Have
1. Adjustable split-screen ratio
2. Dark mode
3. Weather animation overlays
4. Calendar event creation
5. Sunrise/sunset times
6. UV index and air quality

## Non-Functional Requirements

### Performance
- Initial load time < 2 seconds
- API response handling < 1 second
- Smooth animations and transitions

### Usability
- Intuitive navigation
- Clear visual hierarchy
- Accessible (WCAG 2.1 AA compliance)
- Mobile-first responsive design

### Reliability
- Graceful error handling
- Offline capability (cached data)
- API rate limit management

### Security
- Secure API key storage
- HTTPS only
- No sensitive data storage

## Technical Constraints
- Must work on modern browsers (Chrome, Firefox, Safari, Edge)
- Configurable location via LOCATION_LAT and LOCATION_LON environment variables
- OpenWeatherMap One Call API 3.0 (1000 calls/day free tier)
- RainViewer API for radar (free)
- Google Calendar iCal feed URLs required
- Weather refresh: 2 minutes (720 calls/day)
- Calendar refresh: 2 minutes
- Split-screen layout (50/50 or adjustable)
- Must run in single container (Podman or Docker)
- Target platform: Raspberry Pi (ARM architecture)
- Optimized for low resource usage
