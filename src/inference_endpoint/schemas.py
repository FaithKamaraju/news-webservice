from pydantic import BaseModel, ConfigDict
from datetime import datetime



class BodyParamsSingle(BaseModel):
    uuid : str
    scrapped_content : str

class BodyParamsBatch(BaseModel):
    uuids : list[str]
    scrapped_contents : list[str]


class InferenceResultsRespSchema(BaseModel):
    
    uuid : str
    bias_label : str
    bias_score : float
    sentiment_label : str
    sentiment_score : float

