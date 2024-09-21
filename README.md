# fast-api-kube



## fast-api-kube API

### Prerequisites

Docker docker-compose
Install docker and have the daemon running: https://docs.docker.com/get-docker/

### Getting started

- Clone this repo ☝️
  - `cd `
 - Build the container image :sudo scripts/build.sh
 - Bring up the container: sudo scripts/up.sh
 - Check on your browser: <http://localhost:8080/check>
  
### For Devlopper

activate venv : env\Scripts\activate


#start  application

fastapi dev main.py

### Interactive API docs
Go to http://127.0.0.1:8000/docs.

You will see the automatic interactive API documentation (provided by Swagger UI)

## Configuration

Defaults in this repo. Please change them to suit your needs:

Python version:

    Dockerfile#1: FROM python:3.9

localhost:PORT -- set to `8000`

_Don't need to change the `8000`, that's set in the Dockerfile and is only used "internally" by that image._

    docker-compose.yaml#7:    - 8000:8000


image name `fastapiapp`

    $ docker build -t fastapiapp .

    docker-compose.yaml#5      image: fastapiapp:latest
