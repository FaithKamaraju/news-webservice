from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from core.db import Base


class NewsArticle(Base):
    """
        'uuid', 'title', 'description', 'url',
       'image_url', 'published_at', 'source', 'categories',
    """
    __tablename__ = 'news_article'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    uuid = Column(String, index=True, unique=True)
    title = Column(String, index=True)
    description = Column(String)
    url = Column(String)
    image_url = Column(String)
    published_at = Column(DateTime(timezone=True), index=True)
    source = Column(String, index=True)
    categories = Column(String)
    
class InferenceResults(Base):
    
    __tablename__ = 'inference_results'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    uuid = Column(String, ForeignKey('news_article.uuid'), index=True, unique=True)
    bias_score = Column(Float, index=True)
    sentiment_score = Column(Float, index=True)

class ScrappedContent(Base):
    
    __tablename__ = 'scrapped_content'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    uuid = Column(String, ForeignKey('news_article.uuid'), index=True, unique=True)
    scrapped_content = Column(String)