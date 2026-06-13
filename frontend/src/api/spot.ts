import api from './index'

export function fetchSpotList(params?: Record<string, any>) {
  return api.get('/spot', { params })
}

export function fetchSpotTrend(region: string, days: number = 30) {
  return api.get('/spot/trend', { params: { region, days } })
}
