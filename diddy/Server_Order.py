
class Server_Order:
    def __init__(self):
        self.msg = None
        self.has_been_modified = False

    def change_msg(self, msg) -> None:
        self.has_been_modified = True
        self.msg = msg
    
    def get_msg(self) -> str :
        self.has_been_modified = False
        return self.msg

    def get_has_been_modified(self) -> bool:
        return self.has_been_modified