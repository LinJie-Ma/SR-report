import api from './index'

export function fetchNewsList(params?: Record<string, any>) {
  return api.get('/news', { params })
}
