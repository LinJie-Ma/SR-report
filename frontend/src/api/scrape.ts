import { scrapeApi } from './index'

export function triggerScrape() {
  return scrapeApi.post('/scrape/trigger?data_type=all')
}
