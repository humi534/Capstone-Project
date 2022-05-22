import tkinter as tk
from Warehouse import Warehouse

#Colors:
BACKGROUND = "#807777"
TEXT_BACKGROUND = "#c7c1c1"
RED = "red"
YELLOW = "yellow"
BLUE = "blue"
WHITE = "white"
GREEN = "green"
ROBOT = "red"

class GUI(tk.Frame):

    def __init__(self, warehouse:Warehouse):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("Warehouse")
        self.master.resizable(0, 0)

        self.cell_size = 50
        self.warehouse = warehouse

        self.cells_type = warehouse.get_cells_type()
        self.cells_label = warehouse.get_cells_label()

        self.main_grid = tk.Frame(self, bg=BACKGROUND, bd=3, width=self.cell_size*len(self.cells_type), height=self.cell_size*len(self.cells_type[0]))
        self.main_grid.grid(pady=(20,0))
        self.make_GUI()

        self.mainloop()


    def make_GUI(self):
        for i in range(len(self.cells_type)):
            for j in range(len(self.cells_type[0])):
                cell_color = WHITE
                if self.cells_type[i][j] == 0:
                    cell_color = WHITE
                elif self.cells_type[i][j] == 1:
                    cell_color = BLUE
                elif self.cells_type[i][j] == 2:
                    cell_color = GREEN
                elif self.cells_type[i][j] == 3:
                    cell_color = YELLOW
                elif self.cells_type[i][j] == 4:
                    cell_color = RED
                cell_frame = tk.Frame(self.main_grid, bg = cell_color, width=self.cell_size, height=self.cell_size)
                cell_frame.grid(row=i, column=j, padx=1, pady=1)

                if self.cells_label[i][j] != 0:
                    cell_number = tk.Label(self.main_grid, text=self.cells_label[i][j])
                    cell_number.grid(row=i, column=j)
                
        #for robot in self.warehouse.robotsManager.robots:
         #   if robot.direction == "east" or robot.direction == "west":
          #      cell_robot = tk.Frame(self.main_grid, bg = ROBOT, width=self.cell_size/1.5, height=self.cell_size/2)
           # if robot.direction == "north" or robot.direction == "south":
            #    cell_robot = tk.Frame(self.main_grid, bg = ROBOT, width=self.cell_size/2, height=self.cell_size/1.5)
            #cell_robot.grid(row=robot.posX, column=robot.posY)

    def mainloop(self):
        self.master.mainloop()