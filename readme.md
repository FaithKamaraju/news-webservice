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

# TO-DO

- [ ] Make the backend for the news aggregation. Contains no model deployments
- [ ] Spin up a postgresql database for storing news article information
  - [ ] Experiment with the newsapi and try to pull some data that I can use to develop the app and the database
- [ ] Make a frontend that connects to the webserver and displays the articles
  - [ ] make a prototype design in powerpoint or some other software
  - [ ] Look at some other news sites and get some ideas
- [ ] Deploy the HF model on paperspace gradient and add the functionality of toxicity and bias analysis
- [ ] Use docker compose to spin up a dev version of the whole app - the model inferencing can happen on the fastapi backend for now.
- [ ]

## System Flow

1. The React frontend interacts with the FastAPI web server to fetch and display data.
2. The FastAPI web server:
   - Pulls data from an external API.
   - Updates the PostgreSQL database with the new data.
3. The Transformer model service:
   - Fetches relevant data from the PostgreSQL database.
   - Performs inference and updates the database with processed results.
4. The FastAPI web server:
   - Retrieves the processed inferences and raw data from the database.
   - Sends the combined results to the React frontend.

