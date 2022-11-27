from typing import List
import re

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .fake_cache import fake_cache

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Converts a URL into its base URL form
# See for details: https://code.tutsplus.com/tutorials/8-regular-expressions-you-should-know--net-6149
def convert_to_base_URL(url : str):
    base_url = ""
    match = re.search(r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?', url)
    if match:
        if match.group(2) and match.group(3):
            base_url = match.group(2) + "." + match.group(3)
    else:
        print("Enter valid URL")
    return base_url
    
class URLApi:
    def __init__(self):
        pass

    # GET request to read the DB. Returns an object defined by schemeas.URL_look_up
    @app.get("/v1/urlinfo/", response_model = schemas.URL_look_up)
    def read_url(resource_url_with_query_string: str, db: Session = Depends(get_db)):
        # Convert the URL into the format www.google.com to match the way the POST stores into the db
        base_url = convert_to_base_URL(resource_url_with_query_string)
        
        # Use a cache of the worlds most popular websites instead of querying db
        if base_url in fake_cache:
            return {"url": base_url, "allowed": fake_cache[base_url]}

        db_url = crud.get_url(db, url_query = base_url)
        if db_url is None:
            raise HTTPException(status_code=404, detail="URL not found")
        return db_url

    # POST request to update the DB using the URL_look_up_create JSON model
    @app.post("/urlset/", response_model=schemas.URL_look_up_create)
    def create_url(
        urlSchema: schemas.URL_look_up_create, db: Session = Depends(get_db)
    ):
        base_url = convert_to_base_URL(urlSchema.url)
        if not base_url:
            raise HTTPException(status_code=400, detail="Not a valid URL")
        
        urlSchema.url = base_url
        return crud.create_url(db=db, urlSchema=urlSchema)
