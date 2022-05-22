from QRData import QRData

class QRProduct(QRData):
    def __init__(self, img=None) -> None:
        super().__init__()
        self.target: tuple = None

        if img != None:
            self.newQRProduct(img)


    def newQRProduct(self, img) -> None:
        data = super().barcode(img)
        if data["isProduct"]:
            if self.target != data["target"]:
                self.target = data["target"]
                self.has_been_modified = True

    def toString(self) -> str:
        s = "QR Product:"
        s += "\t"
        s += str("has been modified: " + self.has_been_modified)
        s += "\n"
        s += str("target: " + self.target)
        s += "\n"
        return s
