
class Path:
    
    def __init__(self, path: list = []) -> None:
        """
            path is defined as a list of list, each element containing a position (tuple) and an order
            order can either be 'left', 'right' or 'straight' if during path but the the final order must be 
            either 'scan', 'eject' or 'charge'
            example:  [[(1,1),"straight"], [(1,2), "straight"], [(1,3), 'scan']]   
        """
        self.newPath(path)

    def newPath(self, path:list) -> None:
        self.clear()
        for i in range(len(path)):
            self.list_pos.append(path[i][0])
            self.list_order.append(path[i][1])
    
    def updatePosition(self, newPos:tuple) -> None:
        self.index = self.list_pos.index(newPos)

    def destinationReached(self) -> bool:
        """Return True if the final position is reached, False otherwise"""
        return self.index == len(self.list_pos)-1

    def checkPositionInPath(self, pos:tuple) -> bool:
        if pos in self.list_pos:
            return True
        return False

    def getFinalOrder(self) -> str:
        """Returns the last order, which is either 'scan', 'eject', or 'charge'. """
        return self.list_order[-1]

    def getCurrentPosition(self) -> tuple:
        return self.list_pos[self.index]
        
    def getOrderFromIndex(self, index:int):
        return self.list_order[index]

    def getOrderFromPosition(self, position:tuple):
        return self.list_order[self.list_pos.index(position)]

    def clear(self):
        self.index = 0
        self.list_pos = []      #list of tuples
        self.list_order = []    #list of str

    def toString(self):
        s = "Path:"
        for i in range(len(self.list_pos)):
            s += "\t"
            s += str(self.list_pos[i])
            s += "\t"
            s += str(self.list_order[i])
            s += "\n"
        return s
