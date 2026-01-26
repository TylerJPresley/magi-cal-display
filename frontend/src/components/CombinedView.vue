<template>
  <div class="combined-view">
    <!-- Weather Alerts (Full Width) -->
    <div v-if="weatherStore.data?.alerts?.length > 0" class="alerts-section">
      <div v-for="alert in weatherStore.data.alerts" :key="alert.event" class="alert-item">
        <div class="alert-header">
          <span class="alert-icon">⚠️</span>
          <span class="alert-event">{{ alert.event }}</span>
          <span class="alert-dates">
            {{ formatAlertDate(alert.start) }} - {{ formatAlertDate(alert.end) }}
          </span>
        </div>
        <div class="alert-description">{{ alert.description }}</div>
      </div>
    </div>

    <!-- Drive Time Alerts -->
    <div v-if="driveTimeAlerts.length > 0" class="drive-alerts-section">
      <div class="drive-alert-item">
        <span class="drive-alert-icon">🚗</span>
        <span class="drive-alert-label">Traffic Delay:</span>
        <span v-for="(drive, i) in driveTimeAlerts" :key="drive.name" class="drive-alert-entry">
          <span class="drive-alert-name">{{ drive.name }}</span>
          <span class="drive-alert-delay">+{{ drive.traffic_delay_minutes }} min</span>
          <span v-if="i < driveTimeAlerts.length - 1" class="drive-alert-sep">·</span>
        </span>
      </div>
    </div>

    <!-- I-40 Status -->
    <div v-if="i40Status?.has_delay" class="i40-alert">
      <span class="i40-icon">⚠️</span>
      <span class="i40-label">I-40 Conway → Little Rock:</span>
      <span class="i40-delay">+{{ i40Status.delay_minutes }} min</span>
      <span v-if="i40Status.reason" class="i40-reason">— {{ i40Status.reason }}</span>
    </div>

    <!-- Main Content: Weather and Calendar -->
    <div class="main-content">
      <!-- Weather Section -->
      <div class="weather-column">
        <!-- Today's Outlook -->
        <div class="current-overview">
      <div class="overview-content">
        <!-- Left: Weather + Hourly + Calendar -->
        <div class="overview-left">
          <div v-if="weatherStore.data" class="current-header">
            <div class="top-row">
              <div class="condition-icon">{{ getWeatherIcon(weatherStore.data.current.weather[0].main) }}</div>
              <div class="temp-section">
                <div class="temp-large">{{ Math.round(weatherStore.data.current.temp) }}°F</div>
              </div>
              <div class="wind-compass">
                <svg viewBox="0 0 120 120" class="compass-svg">
                  <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2"/>
                  <text x="60" y="20" text-anchor="middle" class="compass-label">N</text>
                  <text x="105" y="65" text-anchor="middle" class="compass-label">E</text>
                  <text x="60" y="108" text-anchor="middle" class="compass-label">S</text>
                  <text x="15" y="65" text-anchor="middle" class="compass-label">W</text>
                  <g :transform="'rotate(' + weatherStore.data.current.wind_deg + ' 60 60)'">
                    <path d="M 60 30 L 65 55 L 60 50 L 55 55 Z" fill="#4ecdc4"/>
                    <line x1="60" y1="55" x2="60" y2="75" stroke="#4ecdc4" stroke-width="3"/>
                  </g>
                </svg>
                <div class="wind-speed">{{ Math.round(weatherStore.data.current.wind_speed) }} mph</div>
              </div>
              <div class="condition-section">
                <div class="condition">{{ weatherStore.data.current.weather[0].description }}</div>
                <div class="feels-like">Feels like {{ Math.round(weatherStore.data.current.feels_like) }}°</div>
                <div class="high-low">
                  <span class="high">H: {{ Math.round(weatherStore.data.daily[0].temp.max) }}°</span>
                  <span class="low">L: {{ Math.round(weatherStore.data.daily[0].temp.min) }}°</span>
                </div>
              </div>
            </div>
            <div v-if="weatherStore.data.daily && weatherStore.data.daily[0].summary" class="daily-summary">
              {{ weatherStore.data.daily[0].summary }}
            </div>
          </div>

          <div v-if="weatherStore.data" class="weather-card">
            <div class="extra-details">
              <div class="detail-item">
                <span class="detail-label">🌧️ Rain</span>
                <span class="detail-value">{{ Math.round((weatherStore.data.daily[0].pop || 0) * 100) }}%</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">💧 Humidity</span>
                <span class="detail-value">{{ weatherStore.data.current.humidity }}%</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">☁️ Cloud Cover</span>
                <span class="detail-value">{{ weatherStore.data.current.clouds }}%</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">🔽 Pressure</span>
                <span class="detail-value">{{ weatherStore.data.current.pressure }} mb</span>
              </div>
              <div class="detail-item detail-item-wide">
                <span class="detail-label">🌅 Sun Rise/Set</span>
                <span class="detail-value">{{ formatTime(weatherStore.data.current.sunrise) }} / {{ formatTime(weatherStore.data.current.sunset) }}</span>
              </div>
              <div class="detail-item detail-item-wide">
                <span class="detail-label">🌙 Moon Rise/Set</span>
                <span class="detail-value">{{ formatTime(weatherStore.data.daily[0].moonrise) }} / {{ formatTime(weatherStore.data.daily[0].moonset) }}</span>
              </div>
            </div>

            <div v-if="weatherStore.data.air_quality" class="air-quality-section">
              <div class="air-quality-header">
                <span class="air-quality-title">🌫️ Air Quality</span>
                <div class="aqi-scale">
                  <div class="aqi-scale-bar">
                    <div class="aqi-scale-fill" :style="{ width: (weatherStore.data.air_quality.main.aqi * 20) + '%' }" :class="'aqi-' + weatherStore.data.air_quality.main.aqi"></div>
                    <div class="aqi-scale-marker" :style="{ left: (weatherStore.data.air_quality.main.aqi * 20) + '%' }">
                      <span class="aqi-value">{{ weatherStore.data.air_quality.main.aqi }}</span>
                    </div>
                  </div>
                  <div class="aqi-scale-labels">
                    <span>Good</span>
                    <span>Fair</span>
                    <span>Moderate</span>
                    <span>Poor</span>
                    <span>Very Poor</span>
                  </div>
                </div>
              </div>
              <div class="pollutants-row">
                <span class="pollutant-compact">PM2.5 <strong>{{ weatherStore.data.air_quality.components.pm2_5.toFixed(1) }}</strong></span>
                <span class="pollutant-compact">PM10 <strong>{{ weatherStore.data.air_quality.components.pm10.toFixed(1) }}</strong></span>
                <span class="pollutant-compact">O₃ <strong>{{ weatherStore.data.air_quality.components.o3.toFixed(1) }}</strong></span>
                <span class="pollutant-compact">NO₂ <strong>{{ weatherStore.data.air_quality.components.no2.toFixed(1) }}</strong></span>
              </div>
            </div>
          </div>

          <!-- Hourly Forecast -->
          <div v-if="weatherStore.data" class="hourly-section">
            <div class="hourly-labels">
              <div v-for="hour in getHourlyForecast()" :key="hour.dt" class="hour-label-item">
                <div class="hour-icon-small">{{ getWeatherIcon(hour.weather[0].main) }}</div>
                <div class="hour-temp">{{ Math.round(hour.temp) }}°</div>
                <div class="hour-time-small">{{ formatHourWithDay(hour.dt) }}</div>
              </div>
            </div>
          </div>

          <!-- Calendar -->
          <div class="upcoming-section">
            <div v-for="(day, index) in getNext5Days()" :key="day.date" class="day-row">
              <div class="day-header" :style="{ borderBottom: day.events.length > 0 ? 'none' : '', marginBottom: day.events.length > 0 ? '0.5rem' : '0', paddingBottom: day.events.length > 0 ? '0.5rem' : '0' }">
                <div class="day-name">{{ index === 0 ? 'Today' : day.name }}</div>
                <div v-if="index === 0" class="week-number">Week {{ getWeekNumber(day.date) }}</div>
                <div v-else class="day-weather">
                  <span class="weather-icon">{{ getWeatherIcon(day.weather.main) }}</span>
                  <span class="temp-range">{{ Math.round(day.high) }}° / {{ Math.round(day.low) }}°</span>
                </div>
              </div>
              <div class="day-events">
                <div v-if="day.events.length > 0" class="event-list-compact">
                  <div v-for="event in day.events" :key="event.id" class="event-compact" :class="{ 'event-past': isEventPast(event) }">
                    <span class="event-time-small">{{ formatEventTime(event) }}</span>
                    <div class="event-details-small">
                      <span class="event-title-small">{{ event.summary }}</span>
                    </div>
                    <div class="event-meta-small">
                      <span class="event-calendar-small">{{ getCalendarName(event.calendar_index) }}</span>
                      <span class="event-location-small">{{ event.location || 'Location Unknown' }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Clock + Drive Times + Traffic Map -->
        <div class="overview-right">
          <div class="clock-section">
            <div class="clock-time">{{ formatClockTime() }}</div>
            <div class="clock-date-row">
              <span class="clock-date">{{ formatClockDate() }} – Week {{ getWeekNumber(currentTime.toDateString()) }}</span>
            </div>
          </div>
          <!-- Drive Times -->
          <div class="drive-times-section">
            <div v-if="driveTimesLoading" class="loading-drive-times">
              <div class="loading-spinner"></div>
              <span>Calculating routes...</span>
            </div>
            <div v-else-if="driveTimes.length > 0" class="drive-times-grid">
              <div v-for="drive in driveTimes" :key="drive.name" class="detail-item">
                <span class="detail-label">{{ drive.name }}</span>
                <span class="detail-value">{{ drive.travel_time_minutes }} min</span>
                <span class="drive-detail-sub">
                  {{ drive.distance_miles }} mi<template v-if="drive.traffic_delay_minutes > 0"> · <span class="drive-delay-inline">+{{ drive.traffic_delay_minutes }} min</span></template>
                </span>
              </div>
            </div>
            <div v-else class="no-drive-times">No destinations configured</div>
          </div>
          <!-- Traffic Map -->
          <div class="traffic-map-box">
            <div id="traffic-map"></div>
          </div>
        </div>
      </div>
    </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, computed, ref } from 'vue'
import { useWeatherStore } from '../stores/weather'
import { useCalendarStore } from '../stores/calendar'

const weatherStore = useWeatherStore()
const calendarStore = useCalendarStore()

let map = null
let trafficMap = null
let radarLayer = null
const hourlyIndices = ref([1, 2, 4, 8, 12, 24])
const hereApiKey = ref('')
const openWeatherKey = ref('')
const driveTimes = ref([])
const homeCoords = ref(null)
const driveTimesLoading = ref(false)
const currentTime = ref(new Date())

const i40Status = ref(null)

const driveTimeAlerts = computed(() => {
  return driveTimes.value.filter(d => d.traffic_delay_minutes > 8)
})
let clockInterval = null

onMounted(async () => {
  // Fetch configuration from backend
  const config = await fetchConfig()
  weatherStore.startAutoRefresh(config.refreshInterval)
  calendarStore.startAutoRefresh(config.refreshInterval)
  hereApiKey.value = config.hereApiKey
  openWeatherKey.value = config.openWeatherApiKey
  initRadar()
  
  // Fetch drive times first, then init map with proper bounds
  await fetchDriveTimes()
  initTrafficMap()

  clockInterval = setInterval(() => { currentTime.value = new Date() }, 1000)

  await fetchI40Status()

  // Refresh drive times and I-40 status every 2 minutes
  setInterval(async () => {
    await fetchDriveTimes()
    renderRouteTraffic()
    await fetchI40Status()
  }, 120000)
})

onUnmounted(() => {
  if (map) map.remove()
  if (trafficMap) trafficMap.remove()
  if (clockInterval) clearInterval(clockInterval)
  weatherStore.stopAutoRefresh()
  calendarStore.stopAutoRefresh()
})

async function fetchDriveTimes() {
  driveTimesLoading.value = true
  try {
    const response = await fetch('/api/drive-times')
    const data = await response.json()
    driveTimes.value = data.drive_times || []
    homeCoords.value = data.home_coords || null
    
    // Update map bounds if map exists
    if (trafficMap && driveTimes.value.length > 0 && homeCoords.value) {
      const L = window.L
      const bounds = L.latLngBounds([
        [homeCoords.value.lat, homeCoords.value.lon],
        ...driveTimes.value.map(d => [d.lat, d.lon])
      ])
      trafficMap.fitBounds(bounds, { padding: [20, 20] })
    }
  } catch (error) {
    console.error('Failed to fetch drive times:', error)
  } finally {
    driveTimesLoading.value = false
  }
}

async function fetchI40Status() {
  try {
    const response = await fetch('/api/i40-status')
    i40Status.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch I-40 status:', error)
  }
}

async function fetchConfig() {
  try {
    const response = await fetch('/api/health')
    const data = await response.json()
    const indices = data.config?.hourly_indices 
      ? data.config.hourly_indices.split(',').map(i => parseInt(i.trim()))
      : [1, 2, 3, 4, 5, 6, 8, 12, 20, 28, 38, 47]
    return {
      refreshInterval: (data.config?.refresh_interval || 120) * 1000,
      hourlyIndices: indices,
      hereApiKey: data.config?.tomtom_api_key || '',
      openWeatherApiKey: data.config?.openweather_api_key || ''
    }
  } catch (error) {
    console.error('Failed to fetch config, using defaults:', error)
    return {
      refreshInterval: 120000,
      hourlyIndices: [1, 2, 3, 4, 5, 6, 8, 12, 20, 28, 38, 47]
    }
  }
}

function initRadar() {
  // Load Leaflet dynamically
  const link = document.createElement('link')
  link.rel = 'stylesheet'
  link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
  document.head.appendChild(link)

  const script = document.createElement('script')
  script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
  script.onload = () => {
    setTimeout(() => {
      const L = window.L
      if (!document.getElementById('radar-map')) return  // radar removed; Leaflet still loaded for traffic map
      map = L.map('radar-map', {
        center: [35.0887, -92.4421],
        zoom: 8,
        zoomControl: false,
        attributionControl: false
      })

      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19
      }).addTo(map)

      // Function to update radar layer
      let radarFrames = []
      let currentFrameIndex = 0
      let animationInterval = null
      let preloadedLayers = []

      const updateRadar = () => {
        fetch('https://api.rainviewer.com/public/weather-maps.json')
          .then(res => res.json())
          .then(data => {
            if (data.radar && data.radar.past.length > 0) {
              // Get last 3 past frames (30 min) and all nowcast frames (30 min future)
              const pastFrames = data.radar.past.slice(-3)
              const futureFrames = data.radar.nowcast || []
              radarFrames = [...pastFrames, ...futureFrames]
              
              // Create preloaded layers
              preloadedLayers = radarFrames.map(frame => {
                return L.tileLayer(`https://tilecache.rainviewer.com/v2/radar/${frame.path}/256/{z}/{x}/{y}/2/1_1.png`, {
                  opacity: 0.6
                })
              })
              
              // Start animation immediately
              if (animationInterval) clearInterval(animationInterval)
              currentFrameIndex = 0
              showFrame()
              animationInterval = setInterval(showFrame, 1000)
            }
          })
      }

      const showFrame = () => {
        if (preloadedLayers.length === 0) return
        
        // Remove current layer
        if (radarLayer) {
          map.removeLayer(radarLayer)
        }
        
        // Add preloaded layer
        radarLayer = preloadedLayers[currentFrameIndex]
        radarLayer.addTo(map)
        
        // Update timestamp overlay
        const frame = radarFrames[currentFrameIndex]
        const timestamp = new Date(frame.time * 1000)
        const now = new Date()
        const diffMinutes = Math.round((timestamp - now) / 60000)
        
        let timeLabel = ''
        if (diffMinutes < 0) {
          timeLabel = `${Math.abs(diffMinutes)} min ago`
        } else if (diffMinutes === 0) {
          timeLabel = 'Now'
        } else {
          timeLabel = `+${diffMinutes} min`
        }
        
        const timestampEl = document.querySelector('.radar-timestamp')
        if (timestampEl) {
          timestampEl.textContent = timeLabel
        }
        
        currentFrameIndex = (currentFrameIndex + 1) % radarFrames.length
      }

      // Initial radar load
      updateRadar()

      // Refresh radar data every 10 minutes
      setInterval(updateRadar, 600000)
      
      // Force map to resize after container is ready
      setTimeout(() => map.invalidateSize(), 500)
    }, 100)
  }
  document.head.appendChild(script)
}

function getTempPoints() {
  const forecast = getHourlyForecast()
  if (!forecast.length) return []
  
  const temps = forecast.map(h => h.temp)
  const minTemp = Math.min(...temps)
  const maxTemp = Math.max(...temps)
  const range = maxTemp - minTemp || 1
  
  return forecast.map((hour, index) => ({
    x: (index / (forecast.length - 1)) * 1000,
    y: 30 + ((maxTemp - hour.temp) / range) * 120,
    temp: Math.round(hour.temp)
  }))
}

function getTempLinePath() {
  const points = getTempPoints()
  if (!points.length) return ''
  
  let path = `M ${points[0].x} ${points[0].y}`
  for (let i = 1; i < points.length; i++) {
    path += ` L ${points[i].x} ${points[i].y}`
  }
  return path
}

function getTempAreaPath() {
  const points = getTempPoints()
  if (!points.length) return ''
  
  let path = `M ${points[0].x} 180`
  path += ` L ${points[0].x} ${points[0].y}`
  for (let i = 1; i < points.length; i++) {
    path += ` L ${points[i].x} ${points[i].y}`
  }
  path += ` L ${points[points.length - 1].x} 180 Z`
  return path
}

function getTempLinePoints() {
  const forecast = getHourlyForecast()
  if (!forecast.length) return ''
  
  const temps = forecast.map(h => h.temp)
  const minTemp = Math.min(...temps)
  const maxTemp = Math.max(...temps)
  const range = maxTemp - minTemp || 1
  
  const points = forecast.map((hour, index) => {
    const x = (index / (forecast.length - 1)) * 1000
    const y = 130 - ((hour.temp - minTemp) / range) * 100
    return `${x},${y}`
  })
  
  return points.join(' ')
}

function getTempBarHeight(temp) {
  const forecast = getHourlyForecast()
  if (!forecast.length) return 50
  
  const temps = forecast.map(h => h.temp)
  const minTemp = Math.min(...temps)
  const maxTemp = Math.max(...temps)
  const range = maxTemp - minTemp || 1
  
  return 20 + ((temp - minTemp) / range) * 60
}

function getTempColor(temp) {
  if (temp >= 80) return '#ff6b6b'
  if (temp >= 70) return '#ffa500'
  if (temp >= 60) return '#4ecdc4'
  if (temp >= 50) return '#45b7d1'
  return '#95a5a6'
}

function getHourlyForecast() {
  if (!weatherStore.data) return []
  const hourly = weatherStore.data.hourly
  return hourlyIndices.value.map(i => hourly[i]).filter(h => h)
}

function formatHourWithDay(timestamp) {
  const date = new Date(timestamp * 1000)
  const today = new Date()
  
  const time = date.toLocaleTimeString('en-US', { hour: 'numeric' })
  
  if (date.toDateString() === today.toDateString()) {
    return time
  } else {
    const day = date.toLocaleDateString('en-US', { weekday: 'short' })
    return `${day} ${time}`
  }
}

function formatClockTime() {
  return currentTime.value.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true })
}

function formatClockDate() {
  return currentTime.value.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })
}

function formatTime(timestamp) {
  const date = new Date(timestamp * 1000)
  return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })
}

function formatAlertDate(timestamp) {
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    hour: 'numeric', 
    minute: '2-digit' 
  })
}

function formatDayShort(timestamp) {
  const date = new Date(timestamp * 1000)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const checkDate = new Date(date)
  checkDate.setHours(0, 0, 0, 0)
  
  if (checkDate.getTime() === today.getTime()) {
    return 'Today'
  }
  return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
}

function getWeekNumber(dateStr) {
  const date = new Date(dateStr)
  const firstDayOfYear = new Date(date.getFullYear(), 0, 1)
  const pastDaysOfYear = (date - firstDayOfYear) / 86400000
  return Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7)
}

function getNext5Days() {
  const days = []
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  for (let i = 0; i <= 5; i++) {
    const date = new Date(today)
    date.setDate(date.getDate() + i)
    const dateStr = date.toDateString()
    
    const dayWeather = weatherStore.data?.daily[i]
    const dayEvents = calendarStore.events.filter(event => {
      const eventStart = new Date(event.start)
      
      if (event.all_day) {
        // For all-day events, check if date falls within range
        eventStart.setHours(0, 0, 0, 0)
        
        if (!event.end) {
          return eventStart.getTime() === date.getTime()
        }
        
        const eventEnd = new Date(event.end)
        eventEnd.setHours(0, 0, 0, 0)
        // End date is exclusive for all-day events
        return eventStart.getTime() <= date.getTime() && eventEnd.getTime() > date.getTime()
      } else {
        // For regular events, just check if they start on this day
        eventStart.setHours(0, 0, 0, 0)
        return eventStart.getTime() === date.getTime()
      }
    }).sort((a, b) => {
      if (a.all_day && !b.all_day) return -1
      if (!a.all_day && b.all_day) return 1
      return 0
    })
    
    days.push({
      date: dateStr,
      name: date.toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' }),
      weather: dayWeather?.weather[0] || { main: 'Clear' },
      high: dayWeather?.temp.max || 0,
      low: dayWeather?.temp.min || 0,
      events: dayEvents
    })
  }
  
  return days
}

function formatHour(timestamp) {
  const date = new Date(timestamp * 1000)
  return date.toLocaleTimeString('en-US', { hour: 'numeric' })
}

function formatEventTime(event) {
  if (event.all_day) return 'All Day'
  const startDate = new Date(event.start)
  const endDate = new Date(event.end)
  const startTime = startDate.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })
  const endTime = endDate.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })
  return `${startTime} - ${endTime}`
}

function getWeatherIcon(condition) {
  const icons = {
    Clear: '☀️',
    Clouds: '☁️',
    Rain: '🌧️',
    Drizzle: '🌦️',
    Thunderstorm: '⛈️',
    Snow: '❄️',
    Mist: '🌫️',
    Fog: '🌫️'
  }
  return icons[condition] || '🌤️'
}

function getCalendarName(index) {
  const names = ['Personal', 'Family', 'Shared']
  return names[index] || `Calendar ${index + 1}`
}

function isEventPast(event) {
  const now = new Date()
  const eventEnd = new Date(event.end)
  return eventEnd < now
}

function getAirQualityLabel(aqi) {
  if (!aqi) return 'N/A'
  const labels = ['Good', 'Fair', 'Moderate', 'Poor', 'Very Poor']
  return labels[aqi - 1] || 'N/A'
}

function getWindDirection(degrees) {
  const directions = ['↑N', '↗NE', '→E', '↘SE', '↓S', '↙SW', '←W', '↖NW']
  const index = Math.round(degrees / 45) % 8
  return directions[index]
}

function initTrafficMap() {
  if (!hereApiKey.value) {
    console.warn('HERE API key not configured')
    return
  }

  setTimeout(() => {
    const L = window.L
    if (!L) {
      console.error('Leaflet not loaded')
      return
    }

    // Calculate initial bounds from POIs if available
    let initialView = {
      center: [34.85, -92.35],
      zoom: 10
    }

    if (driveTimes.value.length > 0 && homeCoords.value) {
      const bounds = L.latLngBounds([
        [homeCoords.value.lat, homeCoords.value.lon],
        ...driveTimes.value.map(d => [d.lat, d.lon])
      ])
      trafficMap = L.map('traffic-map', {
        zoomControl: false,
        attributionControl: false
      })
      trafficMap.fitBounds(bounds, { padding: [50, 50] })
    } else {
      trafficMap = L.map('traffic-map', {
        center: initialView.center,
        zoom: initialView.zoom,
        zoomControl: false,
        attributionControl: false
      })
    }

    // Dark base map
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      maxZoom: 19
    }).addTo(trafficMap)

    // TomTom traffic flow tile overlay
    if (hereApiKey.value) {
      L.tileLayer(`https://api.tomtom.com/traffic/map/4/tile/flow/relative0/{z}/{x}/{y}.png?key=${hereApiKey.value}`, {
        maxZoom: 19,
        opacity: 0.7
      }).addTo(trafficMap)
    }

    // OpenWeatherMap weather overlays
    if (openWeatherKey.value) {
      L.tileLayer(`https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=${openWeatherKey.value}`, {
        maxZoom: 19,
        opacity: 0.35
      }).addTo(trafficMap)
      L.tileLayer(`https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=${openWeatherKey.value}`, {
        maxZoom: 19,
        opacity: 0.5
      }).addTo(trafficMap)
    }

    // Render routes with traffic colors
    renderRouteTraffic()

    // Force map resize
    setTimeout(() => trafficMap.invalidateSize(), 100)
  }, 1000)
}

// Route colors for each destination
const routeColors = ['#4ecdc4', '#ff6b6b', '#ffd93d', '#6bcb77', '#9b59b6', '#3498db']
let routeLayer = null

function renderRouteTraffic() {
  const L = window.L
  if (!L || !trafficMap) return

  // Clear existing routes
  if (routeLayer) {
    trafficMap.removeLayer(routeLayer)
  }
  routeLayer = L.layerGroup().addTo(trafficMap)

  if (!driveTimes.value.length) return

  // Add home marker
  if (homeCoords.value) {
    L.circleMarker([homeCoords.value.lat, homeCoords.value.lon], {
      radius: 8,
      fillColor: '#4ecdc4',
      color: '#fff',
      weight: 2,
      fillOpacity: 1
    }).addTo(routeLayer).bindTooltip('Home')
  }

  driveTimes.value.forEach((route, index) => {
    // Add destination marker
    L.circleMarker([route.lat, route.lon], {
      radius: 6,
      fillColor: routeColors[index % routeColors.length],
      color: '#fff',
      weight: 2,
      fillOpacity: 1
    }).addTo(routeLayer).bindTooltip(route.name)

    if (!route.polyline || route.polyline.length < 2) return

    // Color by delay severity
    let color = '#4ecdc4'   // Teal - no/minimal delay
    let weight = 3
    if (route.traffic_delay_minutes >= 5) {
      color = '#ff9800'     // Orange - moderate delay
      weight = 4
    }
    if (route.traffic_delay_minutes >= 10) {
      color = '#f44336'     // Red - significant delay
      weight = 5
    }

    L.polyline(route.polyline, {
      color: color,
      weight: weight,
      opacity: 0.85
    }).addTo(routeLayer)
  })
}
</script>

<style scoped>
.combined-view {
  min-height: 100vh;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  box-sizing: border-box;
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.weather-column {
  width: 100%;
}

.calendar-traffic-container {
  display: flex;
  gap: 1rem;
  width: 100%;
}

.calendar-column,
.traffic-column {
  flex: 1;
}

/* Portrait: weather on top, calendar and traffic side-by-side below */
@media (orientation: portrait) {
  .main-content {
    flex-direction: column;
  }
  
  .weather-column {
    width: 100%;
  }
  
  .calendar-traffic-container {
    display: flex !important;
    gap: 1rem;
    width: 100%;
  }
  
  .calendar-column,
  .traffic-column {
    flex: 1;
  }
}

.i40-alert {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  padding: 0.6rem 1rem;
  border-radius: 0.25rem;
  border-left: 4px solid #ff9800;
  background: rgba(255, 152, 0, 0.1);
  margin-bottom: 0.5rem;
}

.i40-icon {
  font-size: 1rem;
}

.i40-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #fefefe;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.i40-delay {
  font-size: 0.85rem;
  font-weight: 700;
  color: #ff5252;
}

.i40-reason {
  font-size: 0.85rem;
  color: #e0e0e0;
}

.drive-alerts-section {
  margin-bottom: 0.5rem;
}

.drive-alert-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  background: rgba(78, 205, 196, 0.1);
  border-left: 4px solid #4ecdc4;
  padding: 0.6rem 1rem;
  border-radius: 0.25rem;
}

.drive-alert-icon {
  font-size: 1.1rem;
}

.drive-alert-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #4ecdc4;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.drive-alert-entry {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.drive-alert-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #fefefe;
}

.drive-alert-time {
  font-size: 0.9rem;
  font-weight: 600;
  color: #4ecdc4;
}

.drive-alert-delay {
  font-size: 0.85rem;
  color: #ff5252;
  font-weight: 600;
}

.drive-alert-sep {
  color: #5a6c7a;
  margin: 0 0.15rem;
}

.alerts-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.alert-item {
  background: rgba(255, 152, 0, 0.15);
  border-left: 4px solid #ff9800;
  padding: 1rem;
  border-radius: 0.25rem;
}

.alert-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.alert-icon {
  font-size: 1.25rem;
}

.alert-event {
  font-size: 1rem;
  font-weight: 600;
  color: #fefefe;
  text-transform: uppercase;
  flex: 1;
}

.alert-dates {
  font-size: 0.85rem;
  color: #b8c5d0;
  margin-left: auto;
}

.alert-description {
  font-size: 0.8rem;
  color: #e0e0e0;
  line-height: 1.4;
}

.today-section {
  background: transparent;
  color: #fefefe;
  border-radius: 0;
  padding: 0;
  border: none;
}

h2 {
  margin: 0 0 0.75rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #fefefe;
}

.current-overview {
  margin-bottom: 1.5rem;
}

.overview-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  align-items: stretch;
}

.overview-left {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.overview-right {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.overview-right .radar-container {
  flex: 1;
  min-height: 250px;
  position: relative;
}

.current-header .top-row {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.condition-icon {
  font-size: 4rem;
  line-height: 1;
}

.temp-section {
  display: flex;
  flex-direction: column;
}

.wind-compass {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.15rem;
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  height: 4rem;
}

.compass-svg {
  width: 3rem;
  height: 3rem;
}

.compass-label {
  fill: rgba(255, 255, 255, 0.5);
  font-size: 8px;
  font-weight: 600;
}

.wind-speed {
  font-size: 0.7rem;
  font-weight: 600;
  color: #4ecdc4;
}

.condition-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0;
}

.condition {
  font-size: 1rem;
  line-height: 2rem;
  text-transform: capitalize;
  color: #fefefe;
}

.feels-like {
  font-size: 0.8rem;
  line-height: 1rem;
  color: #b8c5d0;
}

.temp-large {
  font-size: 4rem;
  font-weight: 700;
  line-height: 1;
  color: #fefefe;
}

.high-low {
  display: flex;
  gap: 1rem;
  margin-top: 0;
}

.high, .low {
  font-size: 0.8rem;
  line-height: 1rem;
  color: #cacaca;
}

.weather-card {
  text-align: left;
  width: 100%;
  padding-top: 1rem;
}

.current-header {
  width: 100%;
}

.daily-summary {
  margin-top: 1rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  font-size: 0.9rem;
  line-height: 1.4;
  color: rgba(255, 255, 255, 0.85);
}

.extra-details {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 0.75rem;
  padding-top: 0;
  padding-left: 1rem;
  padding-right: 1rem;
  border-top: none;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  align-items: flex-start;
}

.detail-item-wide {
  grid-column: span 2;
  padding-top: 0.75rem;
  border-top: 2px solid rgba(255, 255, 255, 0.05);
}

.detail-label {
  font-size: 0.7rem;
  color: #8a8a8a;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.detail-value {
  font-size: 1rem;
  font-weight: 600;
  color: #fefefe;
  text-align: left;
}

.air-quality-section {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.05);
}

.air-quality-header {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.air-quality-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.aqi-scale {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.aqi-scale-bar {
  position: relative;
  height: 24px;
  background: linear-gradient(to right, 
    #50f0e6 0%, #50f0e6 20%,
    #50ccaa 20%, #50ccaa 40%,
    #f0e641 40%, #f0e641 60%,
    #ff5050 60%, #ff5050 80%,
    #960032 80%, #960032 100%
  );
  border-radius: 4px;
  overflow: visible;
}

.aqi-scale-fill {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  transition: width 0.3s ease;
}

.aqi-scale-marker {
  position: absolute;
  top: -8px;
  transform: translateX(-50%);
  transition: left 0.3s ease;
}

.aqi-value {
  display: inline-block;
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
  border: 2px solid #fff;
}

.aqi-scale-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.65rem;
  color: rgba(255, 255, 255, 0.6);
}

.aqi-scale-labels span {
  flex: 1;
  text-align: center;
}

.aqi-1 { background: #50f0e6; color: #000; }
.aqi-2 { background: #50ccaa; color: #000; }
.aqi-3 { background: #f0e641; color: #000; }
.aqi-4 { background: #ff5050; color: #fff; }
.aqi-5 { background: #960032; color: #fff; }

.pollutants-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.pollutant-compact {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.8);
  text-align: center;
}

.today-content {
  display: grid;
  grid-template-columns: 30% 70%;
  gap: 1rem;
  align-items: start;
}

.today-details {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.radar-container {
  border-radius: 4px;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.3);
  position: relative;
}

.radar-timestamp {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: #fff;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 600;
  z-index: 1000;
  pointer-events: none;
}

#radar-map {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.hourly-section {
  margin-top: 0.75rem;
  padding: 0.5rem 0;
  background: transparent;
}

.clock-section {
  margin-bottom: 0.75rem;
}

.clock-time {
  font-size: 4rem;
  font-weight: 700;
  line-height: 1;
  letter-spacing: 0.02em;
  color: #e0e0e0;
}

.clock-date-row {
  margin-top: 0.25rem;
}

.clock-date {
  font-size: 1rem;
  color: #b0b0b0;
}

.hourly-chart {
  position: relative;
}

.temp-graph {
  width: 100%;
  height: 140px;
  margin-bottom: 0.5rem;
}

.temp-label {
  fill: #fefefe;
  font-size: 11px;
  font-weight: 600;
}

.hourly-labels {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 0;
  width: 100%;
  margin-top: 0;
}

.hour-label-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.hour-icon-small {
  font-size: 1.1rem;
}

.hour-temp {
  font-size: 0.9rem;
  font-weight: 600;
  color: #4ecdc4;
}

.hour-time-small {
  font-size: 0.7rem;
  color: #b8c5d0;
  white-space: nowrap;
}

.daily-outlook {
  margin-top: 0;
  padding-top: 1.5rem;
  padding-bottom: 0;
  border-top: none;
}

.daily-outlook h3 {
  margin: 0 0 0.75rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #fefefe;
}

.daily-details-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.75rem;
}

.daily-detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  text-align: center;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.25rem;
  position: relative;
  overflow: hidden;
}

.daily-icon {
  position: absolute;
  left: 0.25rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 2rem;
  opacity: 0.15;
  z-index: 0;
}

.daily-label {
  font-size: 0.7rem;
  color: #8a8a8a;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
  position: relative;
  z-index: 1;
}

.daily-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: #fefefe;
  position: relative;
  z-index: 1;
}


.hourly-strip-full {
  margin-top: 0;
  padding-top: 1.5rem;
  padding-bottom: 0;
  border-top: none;
}

.hourly-strip-full h3 {
  margin: 0 0 0.75rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #fefefe;
}

.event-item {
  display: grid;
  grid-template-columns: 20% 1fr auto;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #2c3840;
  border-radius: 4px;
  border-left: 3px solid #1779ba;
  transition: background 0.2s;
}

.event-item:hover {
  background: #394b59;
}

.event-time {
  font-size: 0.9rem;
  color: #fefefe;
  font-weight: 700;
  display: flex;
  align-items: center;
  text-align: left;
}

.event-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  justify-content: center;
}

.event-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: #fefefe;
}

.event-meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  align-items: flex-end;
  text-align: right;
}

.event-calendar {
  font-size: 0.7rem;
  color: #b8c5d0;
  font-style: italic;
}

.event-location {
  font-size: 0.7rem;
  color: #8a8a8a;
  font-style: italic;
}

.upcoming-section {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.day-row {
  background: transparent;
  color: #fefefe;
  border-radius: 4px;
  padding: 0.75rem 0;
  border: none;
  border-bottom: 1px solid #2c3840;
}

.day-row:last-child {
  border-bottom: none;
}

.day-row:first-child .event-compact {
  background: #394b59;
}

.day-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: none;
}

.day-name {
  font-size: 1rem;
  font-weight: 600;
  color: #fefefe;
}

.week-number {
  font-size: 0.85rem;
  color: #b8c5d0;
  font-weight: 400;
}

.day-weather {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #d4dce3;
}

.weather-icon {
  font-size: 1.25rem;
}

.temp-range {
  font-weight: 400;
}

.event-list-compact {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.event-compact {
  display: grid;
  grid-template-columns: 20% 1fr auto;
  gap: 0.75rem;
  padding: 0.5rem 0.6rem;
  background: #2c3840;
  border-radius: 4px;
  border-left: 2px solid #1779ba;
}

.event-compact.event-past {
  opacity: 0.35;
}

.event-time-small {
  font-size: 0.85rem;
  color: #fefefe;
  font-weight: 700;
  display: flex;
  align-items: center;
  text-align: left;
}

.event-details-small {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  justify-content: center;
}

.event-title-small {
  font-size: 0.85rem;
  font-weight: 400;
  color: #fefefe;
}

.event-meta-small {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  align-items: flex-end;
  text-align: right;
}

.event-calendar-small {
  font-size: 0.65rem;
  color: #b8c5d0;
  font-style: italic;
}

.event-location-small {
  font-size: 0.65rem;
  color: #8a8a8a;
  font-style: italic;
}

.no-events, .no-events-small {
  color: #b8c5d0;
  font-size: 0.85rem;
  font-style: italic;
}

.no-events {
  padding: 0.75rem;
  text-align: center;
}

.no-events-small {
  padding: 0.4rem 0.6rem;
}

.drive-times-section {
  border-top: 1px solid rgba(255, 255, 255, 0.15);
  padding: 0.6rem 0;
  margin-bottom: 0.6rem;
}

.traffic-map-box {
  flex: 1;
  background: #1a1a1a;
  border-radius: 0.5rem;
  overflow: hidden;
  min-height: 0;
  position: relative;
}

#traffic-map {
  width: 100%;
  height: 100%;
  position: absolute;
  inset: 0;
}

.drive-times-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 0.75rem;
}

.drive-detail-sub {
  font-size: 0.75rem;
  color: #8a8a8a;
}

.drive-delay-inline {
  font-size: 0.75rem;
  font-weight: 600;
  color: #ff5252;
}

.no-drive-times {
  color: #b8c5d0;
  font-size: 0.9rem;
  font-style: italic;
  text-align: center;
  padding: 2rem 1rem;
}

.loading-drive-times {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 2rem 1rem;
  color: #b8c5d0;
  font-size: 0.9rem;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 3px solid #2c3840;
  border-top: 3px solid #4ecdc4;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Custom map markers - need :deep() for dynamically created elements */
:deep(.custom-marker) {
  background: transparent;
  border: none;
}

:deep(.marker-icon) {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

:deep(.home-icon) {
  width: 32px;
  height: 32px;
  font-size: 1.25rem;
  background: #1e2a32;
  border: 2px solid #4ecdc4;
}

:deep(.dest-icon) {
  width: 28px;
  height: 28px;
  font-size: 0.85rem;
  color: #1a1a1a;
}

:deep(.dest-tooltip) {
  background: rgba(30, 42, 50, 0.95);
  border: 1px solid #4ecdc4;
  border-radius: 4px;
  color: #fefefe;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 4px 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
}

:deep(.dest-tooltip::before) {
  border-top-color: #4ecdc4;
}

:deep(.leaflet-tooltip-top:before) {
  border-top-color: rgba(30, 42, 50, 0.95);
}
</style>
