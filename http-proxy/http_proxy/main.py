from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/v1/urlinfo/", response_model = schemas.URL_look_up)
def read_url(resource_url_with_query_string: str, db: Session = Depends(get_db)):
    db_url = crud.get_url(db, url_query = resource_url_with_query_string)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return db_url

@app.post("/urlset/", response_model=schemas.URL_look_up_create)
def create_url(
    urlSchema: schemas.URL_look_up_create, db: Session = Depends(get_db)
):
    return crud.create_url(db=db, userSchema=urlSchema)
