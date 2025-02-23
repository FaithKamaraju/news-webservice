from datetime import datetime
import aiohttp
from aiohttp.web import HTTPError,HTTPClientError,HTTPBadRequest, HTTPUnauthorized,HTTPNotFound,HTTPInternalServerError,HTTPServiceUnavailable
import os

from pydantic import TypeAdapter

from core.schemas import InferenceResultsRespSchema

inference_port = os.getenv("INT_INFERENCE_PORT")

async def infer_batch(uuids : list[str], scrapped_contents : list[str]):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(f"http://inference_endpoint:{inference_port}/inference/batch",json={"uuid":uuids,"scrapped_content":scrapped_contents}) as resp:
            try:
                resp.raise_for_status()
                inference_results = await resp.json()
                users_list_adapter = TypeAdapter(list[InferenceResultsRespSchema])
                inference_results_valid = users_list_adapter.validate_python(inference_results)
                return inference_results_valid
            except HTTPError as e:
                raise HTTPError(detail="Inference results could not be fetched. Please try again later.")
            
            
async def infer(uuid : str, scrapped_content : str):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(f"http://inference_endpoint:{inference_port}/inference/single",json={"uuid":uuid,"scrapped_content":scrapped_content}) as resp:
            try:
                resp.raise_for_status()
                inference_result = await resp.json()
                return inference_result
            except HTTPError as e:
                raise HTTPError(detail="Inference result could not be fetched. Please try again later.")