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
