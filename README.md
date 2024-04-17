# Developer Scrape API

> Flask REST API with Swagger docs and user authorization using JWT Token/Redis database.

## Table of Contents

- [General Info](#general-information)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [Features](#features)
- [Project Status](#project-status)

## General Information

- REST API with four different sets of endpoints to GET/POST/PUT/DELETE developers, their investments and flats. There is also endpoint for scraping data(scrape files are nor longer supported: for lasted check my other repo [here](https://github.com/owsiej/DeveloperScrapeDjango)) and downloading data in an excel file. All data is being saved into SQLite database using SQLAlchemy.

## Technologies Used

Main techs used in app are:

- Python 3.11
- Flask/Flask-Smorest
- BeautifulSoup4
- Selenium
- SQLite with SQLAlchemy
- Docker
- Redis
- Swagger docs

All versions you can check in [requirement.txt file](https://github.com/owsiej/Developer-Scrape/blob/main/requirements.txt).

## Setup

To make it run:

- install [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- install [pip](https://pip.pypa.io/en/stable/installation/)
- install all requirements in main dir using

```
$ pip install -r requirements.txt
```

- run appropriate docker commands (make sure you have [docker desktop](https://www.docker.com/products/docker-desktop/) installed and running):

```
$ docker-compose build
$ docker-compose up
```

## Features

- six different sets of endpoints to train different things
- user register/login using JWT Token authorization and Redis database
- SQLite database with SQLAlchemy
- Swagger docs with detailed description on every endpoint
- tests written using unittest

## Project Status

Project is no longer being developed. Scrape files are not up to date as whole thing was moved to more scalable version written in Django, which you can find [here](https://github.com/owsiej/DeveloperScrapeDjango). Beside scrape endpoint everything should work just fine.
