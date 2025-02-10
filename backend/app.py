from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from contextlib import asynccontextmanager
import json
# from datetime import datetime
# from apscheduler.schedulers.background import BackgroundScheduler


from core.db import engine, Base, AsyncSessionLocal
from core.schemas import NewsArticleMetaDataSchema
from core.models import NewsArticle, InferenceResults

# from news import api_pull

# news_articles = pd.read_csv("news_articles.csv", index_col=0)
# time_stp = news_articles['published_at'].apply(lambda x: datetime.fromisoformat(x))
# news_articles['published_at'] = time_stp
# news_articles = news_articles.to_dict('records')
    
with open('api_key.json', 'r') as f:
    api_key = json.load(f)['api_key']


# with open('newsarticles.json','r') as f:
#     article_data = json.load(f)

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
    
async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app:FastAPI):
    
    await create_all()
    # async with AsyncSessionLocal() as session:
    #     stmt = text("""
    #         INSERT INTO news_article (uuid, title, description, url, image_url, published_at, source, categories)
    #         VALUES (:uuid, :title, :description, :url, :image_url, :published_at, :source, :categories)
    #     """)
    #     await session.execute(
    #         stmt,news_articles
    #     )
    #     await session.commit()
    # article_data = api_pull.pull_top_news_articles(api_key)
    # db = get_db()
    yield

app = FastAPI(lifespan=lifespan)


# items = [{"name": "Foo"}, {"name": "Bar"}, {"name": "Baz"}]

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

""" 
get_articles -> for frontend to get articles along with inference results
send_articles_for_inference -> to send article content for inference results
get_inference_results -> to recieve inference results back from the model endpoint

"""