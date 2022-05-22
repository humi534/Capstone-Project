
from Charger import Charger

class ChargersManager:
    def __init__(self) -> None:
        self.chargers = []
        self.add_charger(11,2)
        self.add_charger(11,3)
        self.add_charger(11,4)
        self.add_charger(11,8)
        self.add_charger(11,9)
        self.add_charger(11,10)


    def add_charger(self, posX, posY):
        self.chargers.append(Charger(posX, posY))

    def get_empty_charger(self, isTop:bool):
        """
        Parameters:
        isTop: True if the charger is amongs the top 3 chargers, False otherwise
        """

        if isTop:
            for i in range(0,5):
                if not self.chargers[i].isBusy():
                    return self.chargers[i]
        else:
            for i in range(5,0):
                if not self.chargers[i].isBusy():
                    return self.chargers[i]
        

