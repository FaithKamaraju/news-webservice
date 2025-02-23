# TO-DO
## News API module - 

- [x] When the app is started, add a AsyncIO scheduler with one job - pull the latest articles
    - [x] Use the top-article endpoint and pull the first three articles.
    - [x] Check if the articles are already in the database
    - [x] add the meta-data to the database
    - [x] In the same context, scrape the text data from the website using the scraper module.
    - [x] add the scrapped content to the database
    - [x] In the same context, send the scrapped data to the model inference endpoint and await the inference results
    - [x] add the inference results to the database
    - [x] commit and refresh the db
    - [x] close the db session
- [ ] Repeat every 5 mins for one hour everytime the webservice is started.
- [x] Separate the api pulls based on domains.

## Endpoints - 

### Backend - TheNewsAPI
- [x] pull article meta-data (scheduled)

### Frontend - Backend
- [x] get latest news articles for front-page (article-meta-data + inference_results + scrapped_content) - \["/articles/latest", timestamp] -> List\[NewsArticleRespSchema]
- [x] show more button
- [x] get by categories
- [x] Re-run inference