


"""
Order: a single string of characters is send in order to complete the whole process
each order is separeted by a coma (,)
MOV550 = move forward of 550cm
ROTLEF90 = rotate left of 90 degrees
ROTRIG90 = rotate right of 90 degrees
PIST: activate piston, drop the object, then retract piston

A typical instruction: ROTLEF90,MOV500,ROTRIG90,MOV100,PIST,ROTRIG90,MOV200,ROTLEF90,MOV500
"""

class Robot:

    
    id = 1


    """
    Arguments:
    ---------
    port (int) the server port the robot is connected with
    posX (int) position on the x axis of the robot
    posY (int) position on the y axis of the robot
    direction (str) south, north, east, west
    """
    def __init__(self, id, port, time_path, graph) -> None:
        self.id = id
        self.port = port
        self.graph = graph
        self.time_path = time_path
        self.batteryLevel = 100
        self.package = None
    
    def update_pos(self, newPosX:int, newPosY:int) -> None:
        self.posX = newPosX
        self.posY = newPosY

    def update_package(self, prod_num):
        self.package = prod_num

    def rotate(self, direction:str) -> None:
        print("robot ", self.id, " is now oriented ",direction)

    def get_position(self) -> tuple:
        return (self.posX, self.posY)

    def update_batteryLevel(self, batteryLevel):
        self.batteryLevel = batteryLevel
    

    