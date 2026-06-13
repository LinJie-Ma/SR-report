import api from './index'

export function fetchDashboardSummary() {
  return api.get('/dashboard/summary')
}

export function fetchDashboardLatest() {
  return api.get('/dashboard/latest')
}
