from typing import Optional, List

from fastapi import FastAPI, Response
from pydantic import BaseModel


class Item(BaseModel):
    object: str = ""
    entry: List = []


app = FastAPI()


@app.post("/")
async def create_item(data: Item):
    if data.object == "page":
        return Response(content = "OK")