from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from core.db import get_db
from core.schemas import NewsArticleMetaDataSchema, NewsArticleRespSchema
from core.models import NewsArticle, InferenceResults, ScrappedContent

# todays_date = datetime.today().strftime('%Y-%m-%d')

router = APIRouter(
    prefix='/articles',
    tags=['articles']
)

@router.get("/latest")
async def return_latest_articles(timestamp : datetime ,db : AsyncSession = Depends(get_db)) -> list[NewsArticleRespSchema]:
    
    results = await db.execute(select(NewsArticle, ScrappedContent).join(ScrappedContent)\
        .filter(NewsArticle.published_at >= timestamp).order_by(NewsArticle.published_at.desc()))
    
    data = results.tuples().all()
    if len(data) <=0:
        raise HTTPException(status_code=404, detail="No Articles Found")
    article_data = []
    for article in data:
        article_data.append({**article[0].__dict__, **article[1].__dict__})
    return article_data


@router.get("/show_more")
async def show_more_articles(timestamp : datetime ,db : AsyncSession = Depends(get_db)) -> list[NewsArticleRespSchema]:
    
    results = await db.execute(select(NewsArticle, ScrappedContent).join(ScrappedContent)\
        .filter(NewsArticle.published_at <= timestamp).limit(4))
    
    data = results.tuples().all()
    if len(data) <=0:
        raise HTTPException(status_code=404, detail="No Articles Found")
    article_data = []
    for article in data:
        article_data.append({**article[0].__dict__, **article[1].__dict__})
    return article_data


@router.get("/{category}")
async def get_articles_by_category(category : str, db : AsyncSession = Depends(get_db)) -> list[NewsArticleRespSchema]:
    
    results = await db.execute(select(NewsArticle, ScrappedContent).join(ScrappedContent)\
        .filter(NewsArticle.categories.contains(category)).limit(10))
    
    data = results.tuples().all()
    if len(data) <=0:
        raise HTTPException(status_code=404, detail="No Articles Found")
    article_data = []
    for article in data:
        article_data.append({**article[0].__dict__, **article[1].__dict__})
    return article_data

