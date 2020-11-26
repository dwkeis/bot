from typing import Optional, List
from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
import httpx


class Item(BaseModel):
    object: str = ""
    entry: List = []

VERIFY_TOKEN = "zawarudo"
ACCESS_TOKEN = 'EAAEYLiZBkkycBAJMCGDhIxTtyNkh8dQeWD4J4bPZBCgkOho4NVyAvwpJuVaTTHdWEaWM7cTZBXvWIIsDhT71mDBAT0qZBVwbyRpMbLERcbLeEwxfHLuTDR0FvQ6ZAdvBmwJOQre7aMTopZAoBjODyxB4AGKi5Cn2TZCwoLwJNcL4gZDZD'

class Send:
    def message(self,
        recipient_id: str,
        message_text: str,
        access_token: str = ACCESS_TOKEN,
        message_type: str = "UPDATE",
    ):
        r = httpx.post(
            "https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": ACCESS_TOKEN},
            headers={"Content-Type": "application/json"},
            json={
                "recipient": {"id": recipient_id},
                "message": {"text": message_text},
                "messaging_type": "UPDATE",
            },
        )
        r.raise_for_status()


app = FastAPI()

@app.get("/")
async def verify(request : Request):
    if request.query_params.get("hub.mode") == "subscribe" and request.query_params.get(
        "hub.challenge"):
        if (not request.query_params.get("hub.verify_token") == "zawarudo"):
            return Response(content="Verification token mismatch", status_code=403)
        return Response(content=request.query_params["hub.challenge"])
    return Response(content="Required arguments haven't passed.", status_code=400)



@app.post("/")
def create_item(data: Item):
    if data.object == "page":
        for entry in data.entry:
            messaging_events = [
                event for event in entry.get("messaging", []) if event.get("message")
            ]
            for event in messaging_events:
                message = event.get("message")
                sender_id = event["sender"]["id"]
                if message['message'].get('text'):
                	return Send().message(recipient_id=sender_id, message_text=message['text'])
                else:
                	return Send().message(recipient_id=sender_id, message_text="not support")
    return Response(content = "content received", status_code = 200)

