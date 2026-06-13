import api from './index'

export function fetchFuturesList(params?: Record<string, any>) {
  return api.get('/futures', { params })
}

export function fetchKline(params?: Record<string, any>) {
  return api.get('/futures/kline', { params })
}
