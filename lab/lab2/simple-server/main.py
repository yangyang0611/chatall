from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/api/v1/status")
def get_status(request: Request):
    return {"Status": "Ok!", "root_path": request.scope.get("root_path")}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}