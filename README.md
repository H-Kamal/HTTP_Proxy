# URL INFO LOOKUP
Author: Hamza Kamal

# Set Up

## Using Poetry (Recommended)
1. Clone this repository
2. Navigate to the repository
3. Check if you have Poetry installed on your machine through `poetry --version`
   1. If you don't have Poetry installed, install it through following these instructions: [Install Poetry](https://python-poetry.org/docs/#installation)
4. Run `poetry install` in the repository's root.

## Using Pip
1. Run the following commands to install all the required python packages for the project:
   1. `pip install fastapi`
   2. `pip install uvicorn`
   3. `pip install httpx`

# Usage

1. Go to the root of the repository
2. Run the web server:
   1. Using Poetry: `poetry run uvicorn http_proxy.main:app --reload`

Example usage. For details on the usage of the API see the Docs section below.
1. GET: `http://127.0.0.1:8000/v1/urlinfo/?resource_url_with_query_string=www.google.com`
2. POST: 
```
curl -X 'POST' \
  'http://127.0.0.1:8000/urlset/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "www.facebook.com",
  "allowed": true
}'
```

# Docs

The docs have been automatically generated by FastAPI. To access them, run the web-server following the instructions in [Usage](#usage) and enter in the following URL:
`http://127.0.0.1:8000/docs`

FastAPI docs also have a built in sandbox where you can execute GET and POST requests within the browser.


# Testing

Within the `httpx_proxy` directory, run the command `poetry run pytest`. The tests can be found within `test_main.py`

# Design Consideration

I have assumed that a website with malware will also be considered malicious for all of its paths. For example if `www.malicious.com/malware` is malicious, so must be `www.malicious.com/also/malware`. Thus I hold every entry in the database as the base URL. This assumption simplifies the size of the database since it's not required to hold every page of every website. I have also not decided to build the schema of the database as a whitelist or blacklist since the instructions do not make it clear if we want to have a by default allow or by default disallow policy. A whitelist/blacklist design would decrease the size of the db since it creates a default case for all URLs not in the database rather than having to store every URL as either an `allowed = True` or `allow = False`.

**The size of the URL list could grow infinitely, how might you scale this beyond the
memory capacity of the system? Bonus if you implement this**

The solution to this is to scale the database. We can get more machines rather than expanding the resources of a single machine and use a tool like Kubernetes to scale the resources across many servers.  

**The number of requests may exceed the capacity of this system, how might you solve
that? Bonus if you implement this**

A solution to this is to use caching. There are a couple websites which make up the majority of users internet activity. Thus I have implemented a fake_cache which holds the most popular websites on the web and tells whether they are deemed malware or not. Whenever a GET request queries a URL which matches it's base URL with an entry in the cache, it uses the cache rather than query the database since I/O operations and connections over the internet to databases are costly.

It's expected that the number of reads on this database will vastly exceed the number of writes. Thus another thing that can be done is breaking the databases into 2 databases, one being a read only. This will ensure there aren't writes using resources when reads could be done instead.

Users across the globe also have different internet usage. Using different caches or even different databases through the use of sharding for different countries will be useful.

**What are some strategies you might use to update the service with new URLs? Updates
may be as many as 5000 URLs a day with updates arriving every 10 minutes.**

A solution is to use batching. Rather than update the database with one URL at a time, it is better to collect the URLs and only send a single POST request with all the URL entries at once. This will lower the number of POST requests and the number of I/O operations.