

from Warehouse import Warehouse
from GUI import GUI
from Graph import Graph
import time

#this class generate the warehouse, the GUI and the graphs

class Manager:
    def __init__(self) -> None:
        self.warehouse = Warehouse()
        self.A = Graph("A", self.warehouse)
        self.R = Graph("R", self.warehouse)
        self.P = Graph("P", self.warehouse)
        #self.GUI = GUI(self.warehouse)
        time_path = ([])
        time_path.append([(10,2),[time.time(), time.time()+3]])
        print (time_path[0])
        self.warehouse.robotsManager.add_robot(1, None, time_path, self.R.graph)