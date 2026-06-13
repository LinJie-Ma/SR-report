import api from './index'

export function fetchSpotList(params?: Record<string, any>) {
  return api.get('/spot', { params })
}
