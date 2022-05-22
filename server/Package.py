
class Package:

    def __init__(self, product_id, destination, posX, posY) -> None:
        self.destination = destination
        self.posX = posX
        self.posY = posY
        self.product_id = product_id

    def move(self, newPosX, newPosY):
        self.posX = newPosX
        self.posY = newPosY

    def toString(self):
        s = "product id: "
        s += str(self.product_id)
        return s

    
