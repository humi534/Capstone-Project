from Trap import Trap

class TrapsManager:
    def __init__(self) -> None:
        self.traps = []
        
        self.add_trap(1,1,'France')
        self.add_trap(1,3,'France')
        self.add_trap(1,5,'France')
        self.add_trap(1,7,'France')
        self.add_trap(1,9,'France')
        self.add_trap(1,11,'France')

        self.add_trap(3,1,'France')
        self.add_trap(3,3,'France')
        self.add_trap(3,5,'France')
        self.add_trap(3,7,'France')
        self.add_trap(3,9,'France')
        self.add_trap(3,11,'France')
        
        self.add_trap(5,1,'France')
        self.add_trap(5,3,'France')
        self.add_trap(5,5,'France')
        self.add_trap(5,7,'France')
        self.add_trap(5,9,'France')
        self.add_trap(5,11,'France')
        
        self.add_trap(7,1,'France')
        self.add_trap(7,3,'France')
        self.add_trap(7,5,'France')
        self.add_trap(7,7,'France')
        self.add_trap(7,9,'France')
        self.add_trap(7,11,'France')


    def add_trap(self, posX, posY, destination) -> None:
        self.traps.append(Trap(posX, posY, destination))

    def get_trap_by_id(self) -> Trap:
        return next((x for x in self.traps if x.id == id), None)

    def get_trap_by_position(self, posX, posY) -> Trap:
        return next((x for x in self.traps if x.posX == posX and x.posY == posY), None)


    def deactivate_trap(self, id) -> None:
        trap = self.get_trap_by_id()
        trap.deactivate()

    def change_destination_trap(self, id) -> None:
        trap = self.get_trap_by_id()
        trap.change_destination()
