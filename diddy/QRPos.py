from QRData import QRData

class QRPos(QRData):
    def __init__(self, img=None) -> None:
        super().__init__()
        self.pos: tuple = None

        if img != None:
            self.newQRPos(img)


    def newQRPos(self, img) -> None:
        data = super().barcode(img)
        if not data["isProduct"]:
            if self.pos != data["pos"]:
                self.target = data["target"]
                self.has_been_modified = True

    def toString(self) -> str:
        s = "QR Position:"
        s += "\t"
        s += str("has been modified: " + self.has_been_modified)
        s += "\n"
        s += str("pos: " + self.target)
        s += "\n"
        return s
