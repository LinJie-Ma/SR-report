import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'sugar_futures.db')}"

CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

SCRAPE_INTERVALS = {
    "futures": {"hour": "9-15,21-23", "minute": "0", "day_of_week": "1-5"},
    "spot": {"hour": "15", "minute": "30", "day_of_week": "1-5"},
    "fundamentals": {"hour": "9", "minute": "0", "day_of_week": "1"},
    "news": {"hour": "9-15,21-23/2", "minute": "0", "day_of_week": "1-5"},
    "weather": {"hour": "8", "minute": "0"},
    "enso": {"hour": "10", "minute": "0"},
}
