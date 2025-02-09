This is a multi-service architecture that includes the folowing components -

    1. React front-end
    2. fastapi backend
    3. postgresql database
    4. a fastapi model inference endpoint

The architecture of this web service is this -
![architecture diagram](<Webapp architecture mockup.png>)

The architecture is subject to change ofc. I was planning to even split the site scraping module into another service. But that module ended up being too small to warrant another separate webserver.

I plan to just spin up the containers using docker compose whenever I want to read my news (mostly mornings!). But I believe this architecture is perfectly good for deployment on online services. Actually I tried hosting this on *render.com* or *Digitalocean* with the model endpoint being deployed on *paperspace-gradient*. But the model endpoint was prohibitively expensive for a broke student like me (lol).


