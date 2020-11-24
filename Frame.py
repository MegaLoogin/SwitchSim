class Frame:
    def __init__(self, rtype, message, reciever, sender=None):
        self.type = rtype
        self.message = message
        self.reciever = reciever
        self.sender = sender

    def __str__(self):
        return "Method: " + self.type + "<br>Message: " + self.message + "<br>Reciever: " + self.reciever + "<br>Sender: " + self.sender
