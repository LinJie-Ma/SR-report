import api from './index'

export function fetchFundamentals() {
  return api.get('/fundamentals')
}
