from datetime import datetime
import aiohttp
from aiohttp.web import HTTPError,HTTPClientError,HTTPBadRequest, HTTPUnauthorized,HTTPNotFound,HTTPInternalServerError,HTTPServiceUnavailable
import asyncio


def _extract_req_metadata(top_stories_metadata):
    extracted_data = []
    for story in top_stories_metadata['data']:
        if '/video/' in story['url']:
            continue
        timestp = datetime.fromisoformat(story['published_at'])
        top_stories_req_data = {'uuid':story['uuid'], 
                                'title':story['title'], 
                                'description': story['description'],
                                'url': story['url'],
                                'image_url': story['image_url'], 
                                'published_at': timestp, 
                                'source': story['source'], 
                                'categories': str(story['categories'])
                                }
        
        extracted_data.append(top_stories_req_data)
    return extracted_data

async def _fetch_data(session, url, params, retries=3, backoff=2):
    for attempt in range(retries):
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                top_stories = await response.json()
            final_top_stories = _extract_req_metadata(top_stories)
            return final_top_stories
                
        except HTTPError as e:
                if e.status == 429:  # Rate limit exceeded
                    print(f"Too many requests in the past 60 seconds. Rate limit and remaining requests can be found on the X-RateLimit-Limit header.")
                    await asyncio.sleep(backoff)
                    backoff *= 2  # Exponential backoff
                elif e.status == 400:  # Bad request
                    raise HTTPBadRequest(detail="Validation of parameters failed. The failed parameters are usually shown in the error message.")
                elif e.status == 401:  # Unauthorized
                    raise HTTPUnauthorized(detail="Invalid API token.")
                elif e.status == 402: # Usage limit has been reached
                    raise HTTPClientError(status_code=402, detail="Usage limit of your plan has been reached. Usage limit and remaining requests can be found on the X-UsageLimit-Limit header.")
                elif e.status == 404:  # Not found
                    raise HTTPNotFound(detail="Resource not found. Please check your request parameters.")
                elif e.status == 500:  # Server error
                    raise HTTPInternalServerError(detail="Internal server error. Please try again later.")
                elif e.status == 503:  # Service unavailable
                    raise HTTPServiceUnavailable(detail="Service unavailable. Please try again later.")
                else:
                    raise HTTPError(detail="This status code is not implemented in the error handling.")
    

async def _get_article_metadata_per_domain(session, url, api_key, category):
    
    todays_date = datetime.today().strftime('%Y-%m-%d')
    params = {"api_token":api_key,
          'language':'en',
          'published_on': todays_date,
          'category':category,
          'page':1
          }
    top_stories = await _fetch_data(session=session,url=url,params=params)
    return top_stories
    

async def get_top_article_metadata(api_key, **kwargs):
    article_data = []
    # domains = kwargs.get("domains",["nbcnews.com","vox.com","cbc.ca"])
    categories = kwargs.get("categories",["general","science", "sports", "business", "health", "entertainment", "tech", "politics", "food", "travel"])
    top_url = "https://api.thenewsapi.com/v1/news/top"
    
    async with aiohttp.ClientSession() as session:
        for category in categories:
            top_stories = await _get_article_metadata_per_domain(session, top_url, api_key, category)
            if top_stories:
                article_data = article_data + top_stories
        
    return article_data
















# async def pull_top_news_articles(api_key):
#     article_data = []
    
#     todays_date = datetime.today().strftime('%Y-%m-%d')
             
#     params = {"api_token":api_key,
#           'language':'en',
#           'published_after': todays_date,
#           "domains":domains,
#           'page':1
#           }
#     top_stories = requests.get(top_url,params=params)
#     top_stories = top_stories.json()

#     meta = top_stories['meta']
#     for story in range(len(top_stories['data'])):
#         timestp = datetime.fromisoformat(top_stories['data'][story]['published_at'])
#         top_stories_req_data = {'uuid':top_stories['data'][story]['uuid'], 
#                                 'title':top_stories['data'][story]['title'], 
#                                 'description': top_stories['data'][story]['description'],
#                                 'url': top_stories['data'][story]['url'],
#                                 'image_url': top_stories['data'][story]['image_url'], 
#                                 'published_at': timestp, 
#                                 'source': top_stories['data'][story]['source'], 
#                                 'categories': str(top_stories['data'][story]['categories'])
#                                 }
#         article_data.append(top_stories_req_data)
#     num_full_pages = _get_num_pages(meta['found'])
#     print(num_full_pages)
#     async with aiohttp.ClientSession() as session:
#         tasks = [_fetch_data(session, top_url, api_key, page) for page in range(2, num_full_pages)]
#         results = await asyncio.gather(*tasks)
        
#     squeezed_results = sum(results,[])
#     article_data = article_data + squeezed_results
        
#     return article_data


