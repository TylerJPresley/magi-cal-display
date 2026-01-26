import { defineStore } from 'pinia'
import axios from 'axios'

export const useWeatherStore = defineStore('weather', {
  state: () => ({
    data: null,
    loading: false,
    error: null,
    lastUpdate: null,
    refreshInterval: null
  }),

  actions: {
    async fetchWeather() {
      this.loading = true
      this.error = null

      try {
        const response = await axios.get('/api/weather')
        this.data = response.data
        this.lastUpdate = new Date()
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch weather data'
        console.error('Weather fetch error:', error)
      } finally {
        this.loading = false
      }
    },

    startAutoRefresh(interval = 120000) {
      // Clear existing interval if any
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval)
      }
      
      // Fetch immediately
      this.fetchWeather()
      
      // Set up recurring fetch
      this.refreshInterval = setInterval(() => this.fetchWeather(), interval)
    },

    stopAutoRefresh() {
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval)
        this.refreshInterval = null
      }
    }
  }
})
