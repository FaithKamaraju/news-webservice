# News Webservice with AI powered Political Bias scores


This is a multi-service architecture that includes the folowing components -

    1. NextJs front-end
    2. FastAPI backend
    3. PostgreSQL database
    4. A FastAPI model inference endpoint

The architecture of this web service looks like this -
![architecture diagram](<misc_assets/Webapp architecture mockup.png>)

## What is this?

 - This is a "small" webservice that I built to replace my daily news feeds of google news. I tried ground news but I just found the whole UX extremely noisy and I didn't enjoy reading news there.

 - I took this as a personal project to actually learn docker and docker compose properly this time.

 - This is currently in the v1 phase of the project. I'm only finalizing a prototype right now. For the final version I want to use a Triton inferencing service in-place of the fastapi webserver I have right now. I want to remove all the dependencies of the model deployment as well, 12Gigs of python modules for only inferencing is sily.

## Plans for the future
 - I want to finetune the modernBERT model in a more controlled way. I'm doing a very rushed job right now just to have an inferencing endpoint up and tested.

 - I want to add another model that outputs bias framing of the article texts. I hope to implement ideas from a couple of research papers that delve into the framing bias present in media.

 - I'm going to convert the modernBERT model into an ONNX model and optimize it using TensorRT. I also want to ideally have just the onnx model on a python backend of Triton.

 - I want to make this a small webservice that I can deploy on a homeserver at one point so that my partner can also use it. For this, ideally the model inferencing endpoint is very small in-size.

## My Thoughts on Deployment and Usage

I plan to just spin up the containers using docker compose whenever I want to read my news (mostly mornings!). But I believe this architecture is perfectly good for deployment on online services. Actually I tried hosting this on **render** or **Digitalocean** with the model endpoint being deployed on **paperspace-gradient**. But the model endpoint was prohibitively expensive for a broke student like me (lol).

I actually looked into deploying this on AWS ECS. Free-tier options were too limited imo (maybe still possible?) but if I wanted to get an EC2 instance with a gpu accelerator.. it was expensive again. For the time being, scheduling a windows task to spin up the docker compose everyday is fine for my personal usecase. But apart from some code dedicated for this usecase, everything should be production ready.

After thinking about this for awhile, I think I'm gonna make it as portable as I can and just use it manually for a while. Then when I can afford a home-server, I can just put this little project on it so that I use it on my home network.

## Module workings -- Outdated, will update with new ones soon

1. The NextJs frontend interacts with the FastAPI web server to fetch and display data.
2. The FastAPI web server:
   - Pulls data from an external API. Data is of two types - 
     - Article Metadata - title, image, url, snippet etc. Can use this data for displaying initial results on the news page. When the user clicks the specific article, the full article data is fetched.
     - Article content - article content is scraped using newspaper3k library.
   - Send the new scraped data to the model inference endpoint for bias scores.
   - Updates the PostgreSQL database with the new data.
   - Provides endpoints for the frontend to get article data.
3. The modernBERT model service:
   - Gets relevant data from the the fastapi webserver.
   - Performs inference and returns the results to the webserver.

