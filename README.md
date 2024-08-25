
# Project overview
This project is a simple API that allows you to create, update, delete and list machine learning models. It also allows you to create, update, delete and list machine learning model versions. It is a simple API that allows you to manage machine learning models and their versions.

## FastAPI

## Celery

## Redis

## MongoDB


# Project local setup
Clone the project:
```bash
git clone https://github.com/ssoto/ai-platform-api.git
cd ai-platform-api
```
You are going to need to have [Docker](https://www.docker.com/) installed in your machine or something similar like [Rancher](https://rancher.com/) to run the project.

Then start compiling proper images and running the project:
```bash
docker-compose build  --build-arg ENV=docker workers ai-platform-api 
docker-compose up -d
```
