from pyzbar import pyzbar
import json

class QRData:
    def __init__(self) -> None:
        self.has_been_modified = False

    def barcode(self, img) -> dict:
        """Return the data from the barcode based on the image given"""
        barcodes = pyzbar.decode(img)
        data = None
        for barcode in barcodes:
            print("-------------------------QR Code Detected------------------------")
            print(data)
            barcode_info = barcode.data.decode('utf-8')
            data = json.loads(barcode_info)
        return data

    def checkIfNewData(self) -> bool:
        """Return True if data has been modified,
        Attention: Call this function makes the data not new anymore"""
        temp = self.checkIfNewData
        self.checkIfNewData = False
        return temp

    