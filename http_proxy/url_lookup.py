from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

fake_db = {
    "google.com",
    "https://fastapi.tiangolo.com/",
    "https://facebook.com",
    "www.agar.io"
}

class ProxyResponse(BaseModel):
    url: str
    allowed: bool = False
    databaseLookup: str

class Proxy:
    def __init__(self, response = ProxyResponse):
        self.outResponse = response

    @app.get("/v1/urlinfo/", response_model = ProxyResponse)
    async def url_lookup(resource_url_with_query_string: str):
        database_lookup = "fake_db"
        allowed = False

        if resource_url_with_query_string in fake_db:
            allowed = True
        
        return {"url" : resource_url_with_query_string,
                "allowed" : allowed,
                "databaseLookup" : database_lookup}
        