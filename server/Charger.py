

class Charger:
    def __init__(self, posX, posY) -> None:
        self.posX = posX
        self.posY = posY
        self.isBusy = False

    def set_busy(self, isBusy) -> None:
        self.isBusy = isBusy