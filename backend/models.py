from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Float
from sqlalchemy.dialects.postgresql.array import ARRAY
from db import Base


class NewsArticle(Base):
    """
        'uuid', 'title', 'description','scrapped_content', 'keywords', 'url',
       'image_url', 'published_at', 'source', 'categories',
    """
    __tablename__ = 'news_articles'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    uuid = Column(String, index=True)
    title = Column(String, index=True)
    description = Column(String)
    scrapped_content = Column(String)
    url = Column(String)
    image_url = Column(String)
    published_at = Column(TIMESTAMP, index=True)
    source = Column(String, index=True)
    categories = Column(ARRAY(String, dimensions=1))
    
class InferenceResults(Base):
    
    __tablename__ = 'inference_results'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    uuid = Column(String, ForeignKey('news_articles.uuid'), index=True)
    bias_score = Column(Float, index=True)
    sentiment_score = Column(Float, index=True)
    
    
    