

class Trap:

    nb_trap = 1

    def __init__(self, posX, posY, destination) -> None:
        self.id = Trap.nb_trap
        self.posX = posX
        self.posY = posY
        self.destination = destination
        Trap.nb_trap += 1
        self.active = True

    def deactivate(self):
        self.active = False
    
    def change_destination(self, new_destination):
        self.destination = new_destination