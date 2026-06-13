from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import CORS_ORIGINS
from .database import Base, engine
from .routers import dashboard, enso, fundamentals, futures, news, scrape, spot, weather
from .scheduler import start_scheduler, scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    start_scheduler()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(title="白糖期货信息收集系统", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(futures.router)
app.include_router(spot.router)
app.include_router(fundamentals.router)
app.include_router(news.router)
app.include_router(weather.router)
app.include_router(enso.router)
app.include_router(dashboard.router)
app.include_router(scrape.router)
