# magi-cal-display - Design Mockup

## Visual Layout

### Landscape Mode (Side-by-Side)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ⚠️ Weather Alerts (if any) - Full Width                                    │
├──────────────────────────────────┬──────────────────────────────────────────┤
│  WEATHER COLUMN (Left 50%)       │  CALENDAR COLUMN (Right 50%)             │
├──────────────────────────────────┼──────────────────────────────────────────┤
│                                  │                                          │
│  Current Overview                │  Next 6 Days                             │
│  ┌────────────────────────────┐  │  ┌────────────────────────────────────┐ │
│  │  🌡️ 72°F    💨 8mph SW    │  │  │ Today - Week 4                     │ │
│  │  ☀️ Sunny                  │  │  │ ☀️ 78° / 65°                       │ │
│  │  Feels like 70°            │  │  │                                    │ │
│  │  H: 78° L: 65°             │  │  │ 9:00 AM - Team Meeting             │ │
│  └────────────────────────────┘  │  │ 2:00 PM - Doctor Appointment       │ │
│                                  │  └────────────────────────────────────┘ │
│  Air Quality: Good (AQI 42)      │                                          │
│  PM2.5, PM10, O₃, NO₂, SO₂, CO  │  ┌────────────────────────────────────┐ │
│                                  │  │ Monday, Jan 27                     │ │
│  Hourly Forecast (12 hours)     │  │ ⛅ 75° / 62°                       │ │
│  1h 2h 3h 4h 5h 6h 8h 12h...    │  │                                    │ │
│  ☀️ ☀️ ⛅ ⛅ ☁️ ☁️ 🌧️ 🌧️       │  │ 10:00 AM - Project Review          │ │
│  72° 73° 74° 75° 74° 72° 70° 68°│  └────────────────────────────────────┘ │
│                                  │                                          │
│  Weather Radar                   │  (More days...)                          │
│  [Animated precipitation map]    │                                          │
│                                  │                                          │
└──────────────────────────────────┴──────────────────────────────────────────┘
```

### Portrait Mode (Stacked)

```
┌─────────────────────────────────────┐
│  ⚠️ Weather Alerts (if any)         │
├─────────────────────────────────────┤
│  WEATHER SECTION (Top)              │
├─────────────────────────────────────┤
│                                     │
│  Current Overview                   │
│  🌡️ 72°F  ☀️ Sunny  💨 8mph SW     │
│  Feels like 70° | H: 78° L: 65°    │
│                                     │
│  Air Quality: Good (AQI 42)         │
│                                     │
│  Hourly Forecast                    │
│  1h  2h  3h  4h  5h  6h  8h  12h    │
│  ☀️  ☀️  ⛅  ⛅  ☁️  ☁️  🌧️  🌧️    │
│  72° 73° 74° 75° 74° 72° 70° 68°   │
│                                     │
│  Weather Radar                      │
│  [Animated precipitation map]       │
│                                     │
├─────────────────────────────────────┤
│  CALENDAR SECTION (Bottom)          │
├─────────────────────────────────────┤
│                                     │
│  Today - Week 4                     │
│  ☀️ 78° / 65°                       │
│  9:00 AM - Team Meeting             │
│  2:00 PM - Doctor Appointment       │
│                                     │
│  Monday, Jan 27                     │
│  ⛅ 75° / 62°                       │
│  10:00 AM - Project Review          │
│                                     │
│  (More days...)                     │
│                                     │
└─────────────────────────────────────┘
```

## Key Features

### Responsive Layout
- **Landscape**: Side-by-side columns (weather left, calendar right)
- **Portrait**: Stacked layout (weather top, calendar bottom)
- **Automatic**: Adapts based on screen orientation using CSS media queries

### Weather Display
- Current conditions with temperature, icon, and wind compass
- Air quality index with pollutant breakdown
- 12-hour forecast (selective hours: 1,2,3,4,5,6,8,12,20,28,38,47)
- Animated weather radar with precipitation overlay
- Weather alerts displayed at top when active

### Calendar Display
- Next 6 days (today + 5 future days)
- Each day shows weather icon and temperature range
- Events grouped by day with time, title, and location
- Color-coded by calendar source
- Past events shown with reduced opacity

### No Scrollbars
- Content expands naturally to fit all information
- Page scrolls vertically when content exceeds viewport

## Color Palette

### Primary Colors
- **Background**: `#1a2530` (Dark blue-gray)
- **Text**: `#fefefe` (Off-white)

### Weather Colors
- **Temperature Warm**: `#ff6b6b` (Warm red)
- **Temperature Cool**: `#4ecdc4` (Cool teal)

### Calendar Colors
- Color-coded per calendar source
- Past events: Reduced opacity

## Typography

### Font Family
- **Primary**: `'Open Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif`

## Component Styles

### Weather Alerts
```css
background: rgba(255, 152, 0, 0.15)
border-left: 4px solid #ff9800
padding: 1rem
border-radius: 0.25rem
```

### Calendar Events
```css
background: rgba(255, 255, 255, 0.05)
border-left: 3px solid [calendar-color]
padding: 0.75rem
border-radius: 0.5rem
```

### Radar Map
- Leaflet.js integration
- RainViewer tile overlay
- Auto-updates every 10 minutes

## Responsive Breakpoints

```css
/* Landscape: side-by-side */
@media (orientation: landscape) {
  flex-direction: row;
}

/* Portrait: stacked */
@media (orientation: portrait) {
  flex-direction: column;
}
```
