import { defineStore } from 'pinia'
import axios from 'axios'

export const useCalendarStore = defineStore('calendar', {
  state: () => ({
    events: [],
    loading: false,
    error: null,
    lastUpdate: null,
    refreshInterval: null
  }),

  actions: {
    async fetchEvents() {
      this.loading = true
      this.error = null

      try {
        const response = await axios.get('/api/calendar')
        this.events = response.data.events || []
        this.lastUpdate = new Date()
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch calendar events'
        console.error('Calendar fetch error:', error)
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
      this.fetchEvents()
      
      // Set up recurring fetch
      this.refreshInterval = setInterval(() => this.fetchEvents(), interval)
    },

    stopAutoRefresh() {
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval)
        this.refreshInterval = null
      }
    }
  }
})
