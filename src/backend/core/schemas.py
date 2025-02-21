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
    
class BodyParamsForInferenceSchema(BaseModel):
    
    id : int
    uuid : str
    scrapped_content : str

class InferenceResultsRespSchema(BaseModel):
    
    id : int
    uuid : str
    bias : float
    sentiment_score : float
    
    
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