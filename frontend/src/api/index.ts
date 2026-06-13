import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 15000,
})

const scrapeApi = axios.create({
  baseURL: '/api/v1',
  timeout: 120000,
})

export { scrapeApi }
export default api
