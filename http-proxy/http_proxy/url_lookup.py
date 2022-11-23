from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/v1/urlinfo/")
def read_item(resource_url_with_query_string: str):
    return {"resource_url_with_query_string": resource_url_with_query_string}