import api from './index'

export function fetchWeatherList(params?: Record<string, any>) {
  return api.get('/weather', { params })
}
