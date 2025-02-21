from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
import json
import asyncio
from datetime import datetime, timedelta

from schemas import BodyParamsForInferenceSchema, InferenceResultsRespSchema

from transformers import pipeline
from transformers import PreTrainedTokenizerFast, ModernBertForSequenceClassification

modernbert_tokenizer = PreTrainedTokenizerFast.from_pretrained("./models/ModernBERT-base")
modernbert_model = ModernBertForSequenceClassification.from_pretrained("./models/ModernBERT-base")

classifier = pipeline(
    task="text-classification", 
    model=modernbert_model,
    tokenizer=modernbert_tokenizer,
    device='cuda'
)



app = FastAPI()

@app.get("/inference/single")
def inference_single(body_params : BodyParamsForInferenceSchema) -> InferenceResultsRespSchema:
    print(body_params['uuid'], len(body_params['scrapped_content']))
    result = classifier(body_params['scrapped_content'])
    print(result)
    return {"uuid":body_params['uuid'], 
            "bias_label":result[0]['label'], "bias_score":result[0]['score'], 
            "sentiment_label":"result[1]['label']", "sentiment_score":"result[1]['score']"}
    

@app.get("/inference/batch")
def inference_batch(body_params : list[BodyParamsForInferenceSchema]) -> list[InferenceResultsRespSchema]:
    results = []
    for body_param in body_params:
        result = classifier(body_param['scrapped_content'])
        results.append({"uuid":body_param['uuid'], 
                        "bias_label":result[0]['label'], "bias_score":result[0]['score'], 
                        "sentiment_label":"result[1]['label']", "sentiment_score":"result[1]['score']"})
    return results



@app.get("/")
def inference_root() -> dict[str,str]:
    return {"Hello": "World Hello namste duniya"}


def start_uvicorn(loop):
    config = uvicorn.Config(app,host="0.0.0.0",port=8001 ,loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # start_scheduler(loop)
    start_uvicorn(loop)