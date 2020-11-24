#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot


app = Flask(__name__)
ACCESS_TOKEN = 'EAAEYLiZBkkycBAJMCGDhIxTtyNkh8dQeWD4J4bPZBCgkOho4NVyAvwpJuVaTTHdWEaWM7cTZBXvWIIsDhT71mDBAT0qZBVwbyRpMbLERcbLeEwxfHLuTDR0FvQ6ZAdvBmwJOQre7aMTopZAoBjODyxB4AGKi5Cn2TZCwoLwJNcL4gZDZD'
VERIFY_TOKEN = "zawarudo"
bot = Bot(ACCESS_TOKEN)


#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = message['message']['text']
                    send_message(recipient_id, response_sent_text)

                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run(debug = True, port = 7190)