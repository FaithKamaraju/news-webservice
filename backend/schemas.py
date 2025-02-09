from pydantic import BaseModel, ConfigDict
from datetime import datetime, date, time


class NewsArticleBase(BaseModel):
    
    uuid : str
    title : str
    description : str 
    url : str
    image_url : str
    timestamp : datetime
    source : str
    categories : list[str]

class NewsArticleResp(NewsArticleBase):
    model_config = ConfigDict(from_attributes=True)
    
    summary : str
    bias : float
    toxicity : float

class NewsArticleEnhancedResp(NewsArticleBase):
    model_config = ConfigDict(from_attributes=True)
    
    summary : str
    bias : float
    toxicity : float
    
    
