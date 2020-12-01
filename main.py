"""perform a messenger bot to reply text or non text"""

from typing import List
from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
import httpx


class Item(BaseModel):
    """to build a Item which will receive data from fb json"""

    object: str = ""
    entry: List = [{}]


VERIFY_TOKEN = "zawarudo"
ACCESS_TOKEN = "EAAEYLiZBkkycBAJMCGDhIxTtyNkh8dQeWD4J4bPZBCgkOho4NVy\
                AvwpJuVaTTHdWEaWM7cTZBXvWIIsDhT71mDBAT0qZBVwbyRpMbLERcbLeEwxfHLuTDR0F\
                vQ6ZAdvBmwJOQre7aMTopZAoBjODyxB4AGKi5Cn2TZCwoLwJNcL4gZDZD"


class SendMessage:
    """using httpx to post data back to fb bot"""

    def __init__(
        self,
        recipient_id: str,
        message_text: str,
        # access_token: str = ACCESS_TOKEN,
        # message_type: str = "UPDATE",
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


class NotSupport(SendMessage):
    """using this inherit class if message receive is not support"""

    def __init__(self, recipient_id):
        super().__init__(recipient_id, message_text="Not Support")


app = FastAPI()


@app.get("/")
async def verify(request: Request):
    """use to verify all the info and make sure is the one we need to reply with"""
    if request.query_params.get("hub.mode") == "subscribe" and request.query_params.get(
        "hub.challenge"
    ):
        if not request.query_params.get("hub.verify_token") == "zawarudo":
            return Response(content="Verification token mismatch", status_code=403)
        return Response(content=request.query_params["hub.challenge"])
    return Response(content="Required arguments haven't passed.", status_code=400)


@app.post("/")
async def create_item(data: Item):
    """decrypt the json file and find what contains, finally send reply back"""
    if data.object == "page":
        for entry in data.entry:
            messaging_events = [
                event for event in entry.get("messaging", []) if event.get("message")
            ]
            for event in messaging_events:
                message = event.get("message")
                sender_id = event["sender"]["id"]
                for field in message:
                    if "text" in field:
                        return SendMessage(
                            recipient_id=sender_id, message_text=message["text"]
                        )
                    if "attachment" in field:
                        return SendMessage(
                            recipient_id=sender_id, message_text="Attachment Found."
                        )
    return Response(content="content received", status_code=200)
