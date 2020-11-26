class send:
	def __init__(access_token: str,
    recipient_id: str,
    message_text: str,
    message_type: str = "UPDATE",):
		print("sent")

class send_2(send):
	def massage(self):
		print("sent_2")
		self.message()


send("ACCESS_TOKEN","sender_id","i am")