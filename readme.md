# News Webservice with AI powered Bias and Sentiment Analysis
This is a multi-service architecture that includes the folowing components -

    1. React front-end
    2. fastapi backend
    3. postgresql database
    4. a fastapi model inference endpoint

The architecture of this web service is this -
![architecture diagram](<Webapp architecture mockup.png>)

The architecture is subject to change ofc. I was planning to even split the site scraping module into another service. But that module ended up being too small to warrant another separate webserver.

I plan to just spin up the containers using docker compose whenever I want to read my news (mostly mornings!). But I believe this architecture is perfectly good for deployment on online services. Actually I tried hosting this on *render.com* or *Digitalocean* with the model endpoint being deployed on *paperspace-gradient*. But the model endpoint was prohibitively expensive for a broke student like me (lol).

I actually looked into deploying this on AWS ECS. Free-tier options were too limited imo (maybe still possible?) but if I wanted to get an EC2 instance with a gpu accelerator.. it was expensive again. For the time being, scheduling a windows task to spin up the docker compose everyday is fine for my personal usecase. But apart from some code dedicated for this usecase, everything should be production ready.

## Module workings

1. The React frontend interacts with the FastAPI web server to fetch and display data.
   - I was thinking the react frontend be mostly stateless? I wanna experiment and see how much more stress is put on the backend if the frontend fetches data every refresh.
2. The FastAPI web server:
   - Pulls data from an external API. Data is of two types - 
     - Article Metadata - title, image, url, snippet etc. Can use this data for displaying initial results on the news page. When the user clicks the specific article, the full article data is fetched.
     - Article content - article content is scraped using newspaper3k library.
   - Send the new scraped data to the model inference endpoint for bias and sentiment scores.
   - Updates the PostgreSQL database with the new data.
   - Provides endpoints for the frontend to get article data.
3. The Transformer model service:
   - Fetches relevant data from the PostgreSQL database.
   - Performs inference and updates the database with processed results.
4. The FastAPI web server:
   - Retrieves the processed inferences and raw data from the database.
   - Sends the combined results to the React frontend.

