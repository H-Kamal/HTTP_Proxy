from sqlalchemy.orm import Session

from . import models, schemas


def get_url(db: Session, url_query: str):
    print(db.query(models.URL_Look_Up).filter(models.URL_Look_Up.url == url_query).first())
    return db.query(models.URL_Look_Up).filter(models.URL_Look_Up.url == url_query).first()

def create_url(db: Session, userSchema: schemas.URL_look_up_create):
    db_url = models.URL_Look_Up(url = userSchema.url, allowed = userSchema.allowed)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
