from Graph import Graph
from PackagesManager import PackagesManager
from RobotsManager import RobotsManager
from TrapsManager import TrapsManager
from ChargersManager import ChargersManager
from LoadingZonesManager import LoadingZonesManager


defaultPosX = 5
defaultPosY = 12
WIDTH = 15
HEIGHT = 13
MID = int((HEIGHT-1)/2)

class Warehouse:
    
    def __init__(self) -> None:
        
        self.packagesManager = PackagesManager()

        self.packagesManager.add_package(1, "France", 4, 5)
        self.packagesManager.add_package(2, "France", 4, 3)
        self.packagesManager.add_package(3, "France", 4, 1)
        self.packagesManager.add_package(4, "France", 6, 5)
        self.packagesManager.add_package(5, "France", 6, 3)
        self.packagesManager.add_package(6, "France", 6, 1)
        self.packagesManager.add_package(7, "France", 2, 5)


        self.trapsManager = TrapsManager()
        self.loadingZonesManager = LoadingZonesManager()
        self.chargersManager = ChargersManager()
        self.robotsManager = RobotsManager()


        self.width = WIDTH
        self.height = HEIGHT
        self.picking_cell = ((self.trapsManager.traps[-1].posX+2),MID)


    def get_cells_type(self) -> list:
        """Define the floor type, these things are unmutable, meaning they can not change while running"""

        #Create Grid
        cells_type = []
        for i in range(self.height):
            cells_type.append([])
            for j in range(self.width):
                cells_type[i].append(0) #default value

        #TRAPS
        for trap in self.trapsManager.traps:
            posX = trap.posX
            posY = trap.posY
            cells_type[posY][posX] = 1

        #CHARGERS
        for charger in self.chargersManager.chargers:
            posX = charger.posX
            posY = charger.posY
            cells_type[posY][posX] = 2

        #LOADING ZONES
        for loadingZones in self.loadingZonesManager.loadingZones:
            posX = loadingZones.posX
            posY = loadingZones.posY
            cells_type[posY][posX] = 3


        #TROUBLES
        #à faire

        return cells_type

    def get_cells_label(self) -> list:
        return self.trapsManager.get_cells_label()

    def get_cells_label(self) -> list:
        cells_label = []
        for y in range(self.height):
            cells_label.append([])
            for x in range(self.width):
                trap = self.trapsManager.get_trap_by_position(x,y)
                if trap != None:
                    cells_label[y].append(trap.id)

                else:
                    cells_label[y].append(0)

        return cells_label