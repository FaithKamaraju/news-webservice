import requests
from datetime import datetime, timedelta
import aiohttp
import asyncio
import time

top_url = "https://api.thenewsapi.com/v1/news/top"
domains = "nbcnews.com,vox.com,cbc.ca"

def get_num_pages(num_articles:int):
    articles_left = num_articles%3
    num_full_pages = (num_articles-articles_left)/3
    return 15 if num_full_pages>15 else num_full_pages


async def fetch_data(session, url, api_key,page,retries=3, backoff=2):
    
    todays_date = datetime.today().strftime('%Y-%m-%d')
    yesterday = datetime.now() - timedelta(1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    
    params = {
                "api_token":api_key,
                'language':'en',
                'published_after':yesterday,
                "domains":domains,
                "page":page
            }
    for attempt in range(retries):
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                top_stories = await response.json()
            top_stories_data = top_stories['data']
            final_top_stories = []
            for story in range(len(top_stories_data)):
                top_stories_req_data = {'uuid':top_stories_data[story]['uuid'], 
                                        'title':top_stories_data[story]['title'], 
                                        'description': top_stories_data[story]['description'],
                                        'url': top_stories_data[story]['url'],
                                        'image_url': top_stories_data[story]['image_url'], 
                                        'published_at': top_stories_data[story]['published_at'], 
                                        'source': top_stories_data[story]['source'], 
                                        'categories': top_stories_data[story]['categories']
                                        }
                final_top_stories.append(top_stories_req_data)
        except aiohttp.ClientResponseError as e:
                print(f"HTTP Error: {e}")
                if e.status == 429:  # Rate limit exceeded
                    print(f"Rate limit exceeded. Retrying in {backoff} seconds...")
                    await asyncio.sleep(backoff)
                    backoff *= 2  # Exponential backoff
                elif e.status == 401:  # Unauthorized
                    print("Invalid API key. Please check your API key.")
                    break
                elif e.status == 500:  # Server error
                    print("Server error. Please try again later.")
                    break
                else:
                    print(f"Unhandled HTTP error: {e.status}")
                    break

        except aiohttp.ClientError as e:
            print(f"Request failed: {e}")
            break
    return final_top_stories


async def pull_top_news_articles(api_key):
    article_data = []
    
    todays_date = datetime.today().strftime('%Y-%m-%d')
    yesterday = datetime.now() - timedelta(1)
    yesterday = yesterday.strftime('%Y-%m-%d')
             
    params = {"api_token":api_key,
          'language':'en',
          'published_after':yesterday,
          "domains":domains,
          'page':1
          }
    top_stories = requests.get(top_url,params=params)
    top_stories = top_stories.json()

    meta = top_stories['meta']
    article_data = article_data + top_stories['data']
    num_full_pages = get_num_pages(meta['found'])
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, top_url, api_key, page) for page in range(2, num_full_pages)]
        results = await asyncio.gather(*tasks)
        
    squeezed_results = sum(results,[])
    article_data = article_data + squeezed_results
        
    return article_data

