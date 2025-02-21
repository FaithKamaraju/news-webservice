from pydantic import BaseModel, ConfigDict
from datetime import datetime


class NewsArticleMetaDataSchema(BaseModel):
    """
        'id', 'uuid', 'title', 'description', 'url',
       'image_url', 'published_at', 'source', 'categories',
    """
    id: int
    uuid : str
    title : str
    description : str 
    url : str
    image_url : str
    published_at : datetime
    source : str
    categories : str
    
class InferenceResultsRespSchema(BaseModel):
    
    uuid : str
    bias_score : float
    bias_label :  str
    sentiment_score : float
    sentiment_label : str
    
    
class NewsArticleRespSchema(BaseModel):
    
    uuid : str
    title : str
    description : str 
    url : str
    image_url : str
    published_at : datetime
    source : str
    categories : str
    scrapped_content : str
    # bias : float
    # sentiment_score : float