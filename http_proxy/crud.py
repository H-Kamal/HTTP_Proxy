from sqlalchemy.orm import Session

from . import models, schemas

# READ command from the DB using regex to find all variations of a URL
def get_url(db: Session, url_query: str):
    print(db.query(models.URL_Look_Up).filter(models.URL_Look_Up.url == url_query).first())
    return db.query(models.URL_Look_Up).filter(models.URL_Look_Up.url == url_query).first()

# CREATE an entry to the DB using the URL_look_up_create schema
def create_url(db: Session, urlSchema: schemas.URL_look_up_create):
    db_url = models.URL_Look_Up(url = urlSchema.url, allowed = urlSchema.allowed)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
