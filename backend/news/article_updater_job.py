from news.api_pull import get_top_article_metadata
from news.site_scraper import pull_content_from_url
from sqlalchemy import select
from core.db import async_session_local
from core.models import NewsArticle, ScrappedContent


# stmt = text("""
#             INSERT INTO news_article (uuid, title, description, url, image_url, published_at, source, categories)
#             VALUES (:uuid, :title, :description, :url, :image_url, :published_at, :source, :categories)
#         """)

async def pull_and_add(api_key:str):
    print("Pulling and adding articles")
    article_data = await get_top_article_metadata(api_key)
    
    async with async_session_local() as session :
        for article in article_data:
            exists = await session.scalars(select(NewsArticle).filter(NewsArticle.uuid == article['uuid']))
            if not exists.first():
                news_article = NewsArticle(**article)
                session.add(news_article)
                article_text = pull_content_from_url(article['url'])
                if article_text:
                    scrapped_content = ScrappedContent(uuid=article['uuid'], scrapped_content=article_text)
                    session.add(scrapped_content)
                print(f"Added article {article['title']} to database")
        await session.commit()