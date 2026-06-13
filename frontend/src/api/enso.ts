import api from './index'

export function fetchEnsoList() {
  return api.get('/enso')
}

export function fetchEnsoLatest() {
  return api.get('/enso/latest')
}
