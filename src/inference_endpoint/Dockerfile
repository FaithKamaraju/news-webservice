# syntax=docker.io/docker/dockerfile:1.7-labs

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7
ARG PYTHON_VERSION=3.11.11

FROM python:${PYTHON_VERSION} AS python_base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

WORKDIR /app

# Copy the source code into the container.
COPY ./models/ ./models/

COPY --exclude=./models/ . .

# Expose the port that the application listens on.
EXPOSE 8080

# Run the application.
# CMD ["fastapi", "run", "app.py","--host","0.0.0.0","--port", "8080"]
CMD ["uvicorn", "app:app", "--host","0.0.0.0","--port", "8080"]
# CMD uvicorn 'app:app' --host=0.0.0.0 --port=8000
