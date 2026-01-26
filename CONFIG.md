# magi-cal-display - Configuration Guide

## Environment Variables

The application is configured entirely through environment variables, making it easy to update without rebuilding the container.

### Required Variables

```bash
# OpenWeatherMap API Key
OPENWEATHER_API_KEY=your_api_key_here

# Google Calendar iCal Feed URLs (comma-separated)
ICAL_URLS=https://calendar.google.com/calendar/ical/xxx/basic.ics,https://calendar.google.com/calendar/ical/yyy/basic.ics
```

### Optional Variables

```bash
# Location coordinates (required)
LOCATION_LAT=35.0887
LOCATION_LON=-92.4421

# Refresh interval in seconds (default: 120 = 2 minutes)
REFRESH_INTERVAL=120

# Server port (default: 3000)
PORT=3000
```

## Configuration Methods

### Container Runtime with env.list File (Recommended)

Create `magi-cal-display.env.list` file:

```bash
OPENWEATHER_API_KEY=your_api_key_here
ICAL_URLS=https://calendar.google.com/calendar/ical/xxx/basic.ics,https://calendar.google.com/calendar/ical/yyy/basic.ics
LOCATION_LAT=35.0887
LOCATION_LON=-92.4421
REFRESH_INTERVAL=120
PORT=3000
```

Run with Podman:

```bash
podman run -d \
  --name magi-cal-display \
  --replace \
  -p 3000:3000 \
  --env-file magi-cal-display.env.list \
  --restart always \
  magi-cal-display:latest
```

Or with Docker:

```bash
docker run -d \
  --name magi-cal-display \
  -p 3000:3000 \
  --env-file magi-cal-display.env.list \
  --restart always \
  magi-cal-display:latest
```

### Updating Configuration

Simply edit the env.list file and restart:

```bash
# Edit the file
vim magi-cal-display.env.list

# Restart container to pick up changes (Podman)
podman restart magi-cal-display

# Or with Docker
docker restart magi-cal-display
```

## Getting Google Calendar iCal URLs

1. Go to [Google Calendar](https://calendar.google.com)
2. Click the three dots next to a calendar
3. Select "Settings and sharing"
4. Scroll to "Integrate calendar"
5. Copy the "Secret address in iCal format"
6. Repeat for each calendar you want to display

**Important:** Use the SECRET iCal URL, not the public one, to ensure privacy.

## iCal URL Format

Each URL should look like:
```
https://calendar.google.com/calendar/ical/[calendar-id]/private-[token]/basic.ics
```

Multiple URLs are separated by commas with NO spaces:
```
ICAL_URLS=url1,url2,url3
```

## Example Complete Configuration

```bash
# Weather API
OPENWEATHER_API_KEY=your_api_key_here

# Calendars (Personal, Work, Family)
ICAL_URLS=https://calendar.google.com/calendar/ical/personal@gmail.com/private-abc123/basic.ics,https://calendar.google.com/calendar/ical/work@company.com/private-def456/basic.ics,https://calendar.google.com/calendar/ical/family@gmail.com/private-ghi789/basic.ics

# Location coordinates
LOCATION_LAT=35.0887
LOCATION_LON=-92.4421

# Refresh every 2 minutes
REFRESH_INTERVAL=120

# Run on port 3000
PORT=3000
```

## Systemd Service (Optional)

For automatic startup on Linux systems, create `/etc/systemd/system/magi-cal-display.service`:

**For Podman:**

```ini
[Unit]
Description=magi-cal-display Container
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/podman run --name magi-cal-display --replace -p 3000:3000 --env-file /home/pi/magi-cal-display.env.list magi-cal-display:latest
ExecStop=/usr/bin/podman stop magi-cal-display
Restart=always

[Install]
WantedBy=multi-user.target
```

**For Docker:**

```ini
[Unit]
Description=magi-cal-display Container
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
ExecStartPre=-/usr/bin/docker stop magi-cal-display
ExecStartPre=-/usr/bin/docker rm magi-cal-display
ExecStart=/usr/bin/docker run --name magi-cal-display -p 3000:3000 --env-file /home/pi/magi-cal-display.env.list magi-cal-display:latest
ExecStop=/usr/bin/docker stop magi-cal-display
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable magi-cal-display
sudo systemctl start magi-cal-display
```

Check status:
```bash
sudo systemctl status magi-cal-display
```
