from fastapi import FastAPI, Depends
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
import json
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta


from core.db import get_db, create_all
from news.article_updater_job import pull_and_add

from routers import articles
    
with open('api_key.json', 'r') as f:
    api_key = json.load(f)['api_key']



@asynccontextmanager
async def lifespan(app:FastAPI):
    
    await create_all()
    
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(articles.router)



@app.get("/")
async def read_root() -> dict[str,str]:
    return {"Hello": "World Hello namste duniya"}




def start_scheduler(loop):
    scheduler = AsyncIOScheduler(event_loop=loop)
    start_datetime = datetime.now()
    end_datetime = datetime.now() + timedelta(hours=1)
    scheduler.add_job(pull_and_add,IntervalTrigger(hours=1,start_date=start_datetime,end_date=end_datetime), misfire_grace_time=None ,id="pull_and_add",args=[api_key])

    scheduler.start()

    
def start_uvicorn(loop):
    config = uvicorn.Config(app,host="0.0.0.0",port=8000 ,loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # start_scheduler(loop)
    start_uvicorn(loop)
    

    