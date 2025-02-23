from fastapi import FastAPI, Depends
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta


from core.db import get_db, create_all
from core.models import ScrappedContent, InferenceResults
from core.schemas import InferenceResultsRespSchema
from news.article_updater_job import pull_and_add
from core.inference import infer

from routers import articles

load_dotenv('dev.env')

api_key = os.getenv("API_KEY")
port = int(os.getenv("INT_SERVER_PORT"))


@asynccontextmanager
async def lifespan(app:FastAPI):
    
    await create_all()
    
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(articles.router)



@app.get("/")
async def read_root() -> dict[str,str]:
    return {"Hello": "World Hello namste duniya"}


@app.post("/inference/{uuid}", tags=["inference"])
async def rerun_inference(uuid:str, db : AsyncSession = Depends(get_db)) -> InferenceResultsRespSchema:
    
    result = await db.execute(select(ScrappedContent).filter(ScrappedContent.uuid == uuid))
    scrapped_content = result.scalars().first()
    inference_result = await infer(uuid, scrapped_content.scrapped_content)
    # inference_results_obj = InferenceResults(**inference_result)
    # db.add(inference_results_obj)
    # await db.commit()
    
    return inference_result



def start_scheduler(loop):
    scheduler = AsyncIOScheduler(event_loop=loop)
    start_datetime = datetime.now()
    end_datetime = datetime.now() + timedelta(hours=1)
    scheduler.add_job(pull_and_add,IntervalTrigger(hours=1,start_date=start_datetime,end_date=end_datetime), misfire_grace_time=None ,id="pull_and_add",args=[api_key])

    scheduler.start()

    
def start_uvicorn(loop):
    config = uvicorn.Config(app,host="0.0.0.0",port=port ,loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # start_scheduler(loop)
    start_uvicorn(loop)
    

    