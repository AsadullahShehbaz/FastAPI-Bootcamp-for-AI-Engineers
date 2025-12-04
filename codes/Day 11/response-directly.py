from datetime import datetime
from typing import Union

from fastapi import FastAPI,Response 
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

class Item(BaseModel):
    title: str
    timestamp:datetime
    description: Union[str,None] = None 

app = FastAPI()
@app.get("/")
def read_root():
    return {"Message": "This is tutorial of direct respons with jsonable encoder"}
@app.put("/items/{id}")
def update_item(id: int, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)

# Returning a custom Response
@app.get("/legacy")
async def get_legacy_data():
    data = """
    <html>
        <head>
            <title>Legacy Data</title>
        </head>
        <body>
            <h1>Legacy Data</h1>
            <p>This is legacy data.</p>
            <p>Created by : Ayan Ahmed</p>
        </body>
    </html>
    """
    return Response(content=data, media_type="text/html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)