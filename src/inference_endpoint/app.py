from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

import os
import asyncio

from schemas import InferenceResultsRespSchema, BodyParamsBatch, BodyParamsSingle

from transformers import pipeline
from transformers import PreTrainedTokenizerFast, ModernBertForSequenceClassification
import torch



    
port = int(os.getenv("PORT"))

torch.set_float32_matmul_precision('high')

modernbert_tokenizer = PreTrainedTokenizerFast.from_pretrained("./models/ModernBERT-base")
modernbert_model = ModernBertForSequenceClassification.from_pretrained("./models/ModernBERT-base")

classifier = pipeline(
    task="text-classification", 
    model=modernbert_model,
    tokenizer=modernbert_tokenizer,
    device='cuda'
)



app = FastAPI()

@app.get("/health", tags=["health"])
def health() -> dict[str,str]:
    return {"status": "ok"}

@app.get("/inference/single", tags=['inference'])
def inference_single(body : BodyParamsSingle) -> InferenceResultsRespSchema:
    uuid = body.uuid
    scrapped_content = body.scrapped_content
    print(uuid, len(scrapped_content))
    result = classifier(scrapped_content)
    print(result)
    return {"uuid":uuid,
            "bias_label":result[0]['label'], "bias_score":result[0]['score'], 
            "sentiment_label":"happy", "sentiment_score":0}
    

@app.get("/inference/batch", tags=['inference'])
def inference_batch(body : BodyParamsBatch) -> list[InferenceResultsRespSchema]:
    uuids = body.uuids
    scrapped_contents = body.scrapped_contents
    results = []
    result = classifier(scrapped_contents)
    for uuid, result in zip(uuids,results):
        results.append({"uuid": uuid, 
                    "bias_label":result[0]['label'], "bias_score":result[0]['score'], 
                    "sentiment_label":"happy", "sentiment_score":0})
    return results



@app.get("/")
def inference_root() -> dict[str,str]:
    return {"Hello": "World Hello namste duniya"}


def start_uvicorn(loop):
    config = uvicorn.Config(app,host="0.0.0.0",port=port ,loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_uvicorn(loop)