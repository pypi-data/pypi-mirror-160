class MilaCoinsError(Exception):
    
    def __init__(self, requestID, name,message,code):
        self.requestID = requestID
        self.name = name
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'