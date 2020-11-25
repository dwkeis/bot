from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    object: str = ""
    entry: List = []


app = FastAPI()


@app.post("/")
async def create_item(item: Item):
    return item