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

class InferenceResults(BaseModel):
    
    summary : str
    bias : float
    toxicity : float

class NewsArticleEnhancedResp(NewsArticleBase, InferenceResults):
    model_config = ConfigDict(from_attributes=True)
    
    
