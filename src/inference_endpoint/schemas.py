from pydantic import BaseModel, ConfigDict
from datetime import datetime


    
class BodyParamsForInferenceSchema(BaseModel):
    
    uuid : str
    scrapped_content : str

class InferenceResultsRespSchema(BaseModel):
    
    uuid : str
    bias_label : str
    bias_score : float
    sentiment_label : str
    sentiment_score : float

