from news.api_pull import get_top_article_metadata
from news.site_scraper import pull_content_from_url
from sqlalchemy import select

from core.db import async_session_local
from core.models import NewsArticle, ScrappedContent, InferenceResults
from core.inference import infer_batch


# stmt = text("""
#             INSERT INTO news_article (uuid, title, description, url, image_url, published_at, source, categories)
#             VALUES (:uuid, :title, :description, :url, :image_url, :published_at, :source, :categories)
#         """)

async def pull_and_add(api_key:str):
    print("Pulling and adding articles")
    article_data = await get_top_article_metadata(api_key)
    
    async with async_session_local()as session :
        inference_uuids = []
        inference_content = []
        for article in article_data:
            exists = await session.scalars(select(NewsArticle).filter(NewsArticle.uuid == article['uuid']))
            
            if not exists.first():
                article_text = pull_content_from_url(article['url'])
                
                if article_text:
                    
                    news_article = NewsArticle(**article)
                    
                    scrapped_content = ScrappedContent(uuid=article['uuid'], scrapped_content=article_text)
                    
                    session.add(news_article)
                    session.add(scrapped_content)
                    inference_uuids.append(article['uuid'])
                    inference_content.append(article_text)
                print(f"Added article {article['title']} to database")
                
        inference_results = await infer_batch(inference_uuids, inference_content)
        inference_results_objs = [InferenceResults(**result) for result in inference_results]
        session.add_all(inference_results_objs)
        await session.commit()