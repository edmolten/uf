# UF REST Service

API REST to query UF historic values. Uses Django 2.0 + Django REST Framework 3.7.3 + Scrapy 1.4 + Docker. Tested on Ubuntu 16.04, Windows 10 and masOS Sierra 10.12.6

## Prerequisites

You need [Docker](https://docs.docker.com/engine/installation/) and
[Docker Compose](https://docs.docker.com/compose/install/#install-compose
) to run the service.  

## Setup

1. `cd` to repo
2. Docker commands require root priviligues, so do `sudo su` 
3. The default port in the service is 8000. If it is already used, change 
the value in the `.env` file next to this file
4. Run `docker-compose up -d`. It will take a moment.
5. Fill database with `docker exec -ti ufscrapy bash -c "python run.py populate"`

## Test

- You can manually test the service with `curl` or a browser. Use `http://localhost:PORT/uf/list/` and
 `http://localhost:PORT/uf/price/?value=XXXX&date=yyyymmdd`, changing the port 
- You can also run the unittest with `docker exec -ti ufservice bash -c "python manage.py test uf_app"`
