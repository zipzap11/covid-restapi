# COVID-19 REST-API
Rest api for covid data update, sourced from [Indonesian Government](https://documenter.getpostman.com/view/16605343/Tzm6nwoS).

## Tools
- [python 3](https://docs.python.org/3/tutorial/index.html)
- [fastAPI](https://fastapi.tiangolo.com/)
- [uvicorn](https://www.uvicorn.org/)
- [requests](https://docs.python-requests.org/en/latest/)
- [pytest](https://docs.pytest.org/en/6.2.x/)

## Run
After cloning this repo, you need to install the dependencies needed. Python 3.6 or above is needed or you can just pull the docker image in this [repository-link](https://hub.docker.com/repository/docker/zipzap11/covid-api), or simply run this command
```
docker pull zipzap11/covid-api:1.0
```

If you want to run without container, just install dependencies below. 
#### Install FastAPI
run this command
```
pip3 install fastapi
```

#### Install Uvicorn
run this command
```
pip3 install uvicorn
```

#### Install Requests
run this command
```
pip3 install requests
```

## Run APP
run this command
```
uvicorn app.main:app
```

## Run as Docker Container
First you need to build docker image with this command
```
docker build -t <image-name>:<image-tag> .
```
Example
```
docker build -t zipzap11/covid-api:1.0 .
```
Then run it with
```
docker run -t --name covid-api -p 8000:3000 zipzap11/covid:1.0
```

## Routing
You can see the route documentation by starting the APP and go to `localhost:8000/docs`.
There you can find all the routes provided in swagger UI

## Test
To start unit test, you need to install pytest by simply run
```
pip3 install pytest
```
Then run
```
pytest
```
Unfortunately the unit test does not cover all the possible cases.

