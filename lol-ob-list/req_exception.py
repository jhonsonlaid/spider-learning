
class ReqException(Exception):
    def __init__(self, message):
        super(ReqException, self).__init__()
        self.message = message
