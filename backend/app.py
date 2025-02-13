from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from contextlib import asynccontextmanager
import json
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
# from apscheduler.schedulers.background import AsyncIOScheduler


from core.db import get_db, create_all
from core.schemas import NewsArticleMetaDataSchema
from core.models import NewsArticle, InferenceResults

from news.article_updater_job import pull_and_add

# news_articles = pd.read_csv("news_articles.csv", index_col=0)
# time_stp = news_articles['published_at'].apply(lambda x: datetime.fromisoformat(x))
# news_articles['published_at'] = time_stp
# news_articles = news_articles.to_dict('records')
    
with open('api_key.json', 'r') as f:
    api_key = json.load(f)['api_key']



@asynccontextmanager
async def lifespan(app:FastAPI):
    
    await create_all()
    # await pull_and_add()
    yield

app = FastAPI(lifespan=lifespan)



@app.get("/")
async def read_root() -> dict[str,str]:
    return {"Hello": "World Hello namste duniya"}


@app.get("/articles/all")
async def return_all_articles(db : AsyncSession = Depends(get_db)) -> list[NewsArticleMetaDataSchema]:
    
    results = await db.execute(select(NewsArticle))
    articles = results.scalars().all()
    if len(articles) <=0:
        raise HTTPException(status_code=404, detail="No Articles Found")
    return articles


@app.get("/articles/{n}")
async def return_n_articles(n:int, db: AsyncSession = Depends(get_db)) -> list[NewsArticleMetaDataSchema]:
    
    results = await db.execute(select(NewsArticle))
    articles = results.scalars().all()
    if len(articles) < n:
        return articles
    elif len(articles) <=0:
        raise HTTPException(status_code=404, detail="No Articles Found")
    else:
        return articles[:n]
    

@app.post('/articles')
async def add_articles_to_db(db: AsyncSession = Depends(get_db)):
    pass





def start_scheduler(loop):
    scheduler = AsyncIOScheduler(event_loop=loop)
    start_datetime = datetime.now()
    end_datetime = datetime.now() + timedelta(hours=1)
    scheduler.add_job(pull_and_add,IntervalTrigger(seconds=300,start_date=start_datetime,end_date=end_datetime), misfire_grace_time=None ,id="pull_and_add",args=[api_key])

    scheduler.start()

    
def start_uvicorn(loop):
    config = uvicorn.Config(app,host="0.0.0.0",port=8000 ,loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_scheduler(loop)
    start_uvicorn(loop)
    

    