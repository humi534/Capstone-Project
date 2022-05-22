import networkx as nx
from RobotsManager import RobotsManager
import copy

class Graph:
    
    def __init__(self, name, warehouse) -> None:

        self.warehouse = warehouse
        self.picking_cell = self.warehouse.picking_cell
        self.name = name

        driving_cells = []
        for y in range(self.warehouse.height):
            for x in range(self.warehouse.width):
               driving_cells.append((x,y))
        
        self.chargers = self.warehouse.chargersManager.chargers
        
        #remove traps and loading zones
        self.loadingZones = self.warehouse.loadingZonesManager.loadingZones
        for loadingZone in self.loadingZones:
            driving_cells.remove((loadingZone.posX, loadingZone.posY))

        self.traps = self.warehouse.trapsManager.traps

        for trap in self.traps:
            driving_cells.remove((trap.posX, trap.posY))


        if self.name == 'A':
            #Graph creation
            self.graph = nx.DiGraph()#going (aller) graph
            #----------------
            #Nodes creation
            #----------------
            self.graph.add_nodes_from(driving_cells)
            #-----------------
            #EdgesGraph A
            #-----------------
            self.create_A_edges()
            self.weights_and_directions()

        elif self.name == 'R':
            #Graph creation
            self.graph = nx.DiGraph()#return (retour) graph
            #----------------
            #Nodes creation
            #----------------
            self.graph.add_nodes_from(driving_cells)
            #----------------
            # Edges Graph R
            # --------------- 
            self.create_R_edges()
            self.weights_and_directions()
        
        elif self.name == 'P':
            #Graph creation
            self.graph = nx.DiGraph()#return (retour) graph
            #----------------
            #Nodes creation
            #----------------
            self.graph.add_nodes_from(driving_cells)
            #----------------
            # Edges Graph R
            # --------------- 
            self.create_A_edges()
            self.create_R_edges()
            for x in range((self.traps[0].posX-1), self.picking_cell[0], 2):
                if x > self.traps[0].posX-1:
                    #add up-left and bottom-left from cells on right of the highest and lowest traps 
                    #(same part paths as in A graph but unused in A)
                    y == self.traps[0].posY
                    self.graph.add_edge((x,y), (x-1,y-1), mid=(x,y-1), turn=1, weight=2, direction = 'straight')
                    y == self.traps[-1].posY
                    self.graph.add_edge((x,y), (x-1,y+1), mid=(x,y+1), turn=1, weight=2, direction = 'straight')
                for y in range((self.traps[0].posY-1), (self.traps[-1].posY+2), 2):
                    #add edges from cells that had no edge directly connected (mid cells = cells below-next the traps)
                    #idea: edge of 1 cell in order to get back on "normal" edges
                    if x > 0:
                        self.graph.add_edge((x,y), (x-1,y), mid=0, turn=0, weight=1, direction = 'straight')
                    self.graph.add_edge((x,y), (x+1,y), mid=0, turn=0, weight=1, direction = 'straight')
                    if y > 0:
                        self.graph.add_edge((x,y), (x,y-1), mid=0, turn=0, weight=1, direction = 'straight')
                    if y != self.traps[-1].posY+1:
                        self.graph.add_edge((x,y), (x,y+1), mid=0, turn=0, weight=1, direction = 'straight')
                for y in range(self.traps[0].posY, self.picking_cell[1], 2):
                    #add edges from cells next to traps
                    #above picking cell
                    self.graph.add_edge((x,y), (x-1,y+1), mid=(x,y+1), turn=1, weight=2, direction = 'straight')
                    self.graph.add_edge((x,y), (x+1,y+1), mid=(x,y+1), turn=1, weight=2, direction = 'straight')
                for y in range((self.picking_cell[1]+1), (self.traps[-1].posY+1), 2):
                    #add edges from cells next to traps
                    #below picking cell
                    self.graph.add_edge((x,y), (x-1,y-1), mid=(x,y-1), turn=1, weight=2, direction = 'straight')
                    self.graph.add_edge((x,y), (x+1,y-1), mid=(x,y-1), turn=1, weight=2, direction = 'straight')
                        
            for x in range(self.traps[0].posX, (self.traps[-1].posX+1), 2):
                for y in range((self.traps[0].posY-1), (self.traps[-1].posY+2), 2):
                    #add edges from cells below the traps:
                    if y < self.picking_cell[1]:
                        #down left
                        self.graph.add_edge((x,y), (x-1,y+1), mid=(x-1,y), turn=1, weight=2, direction = 'straight')
                    if y > self.picking_cell[1]:
                        #up left
                        self.graph.add_edge((x,y), (x-1,y-1), mid=(x-1,y), turn=1, weight=2, direction = 'straight')
                    if y > self.traps[0].posY-1:
                        #up right
                        self.graph.add_edge((x,y), (x+1,y-1), mid=(x+1,y), turn=1, weight=2, direction = 'straight')
                    if y < self.traps[-1].posY+1:
                        #down right
                        self.graph.add_edge((x,y), (x+1,y+1), mid=(x+1,y), turn=1, weight=2, direction = 'straight')
                        
            self.weights_and_directions()
            
    def create_A_edges(self):
        #edges departing from cells below the traps
        for x in range(self.traps[0].posX, (self.traps[-1].posX+1), 2):
            for y in range((self.traps[0].posY+1), self.traps[-1].posY, 2):
                if y <= self.picking_cell[1]:
                    self.graph.add_edge((x,y), (x-1,y-1), mid=(x-1,y), turn=1, weight=2, direction = 'straight')
                if y >= self.picking_cell[1]:
                    self.graph.add_edge((x,y), (x-1,y+1), mid=(x-1,y), turn=1, weight=2, direction = 'straight')
                if x-2 > 0:
                    self.graph.add_edge((x,y), (x-2,y), mid=(x-1,y), turn=0, weight=2, direction = 'straight')
        #edges departing from cells on the left of the traps
        for x in range((self.traps[0].posX-1), (self.traps[-1].posX+2), 2):
            for y in range(self.traps[1].posY, (self.picking_cell[1]), 2):
                self.graph.add_edge((x,y), (x,y-2), mid=(x,y-1), turn=0, weight=2, direction = 'straight')
                if (x > 1):
                    self.graph.add_edge((x,y), (x-1,y-1), mid=(x,y-1), turn=1, weight=2, direction = 'straight')
            for y in range((self.picking_cell[1]+1), (self.traps[-1].posY-1),2):
                self.graph.add_edge((x,y), (x,y+2), mid=(x,y+1), turn=0, weight=2, direction = 'straight')
                if (x > 1):
                    self.graph.add_edge((x,y), (x-1,y+1), mid=(x,y+1), turn=1, weight=2, direction = 'straight')

        x = self.picking_cell[0]
        y = self.picking_cell[1]
        self.graph.add_edge((x,y), (x-1,y-1), mid=(x-1,y), turn=1, weight=1, direction = 'straight')
        self.graph.add_edge((x,y), (x-1,y+1), mid=(x-1,y), turn=1, weight=1, direction = 'straight')
        self.graph.add_edge((x,y), (x-2,y), mid=(x-1,y), turn=0, weight=2, direction = 'straight')
    
    def create_R_edges(self):
        #edges departing from cells on the left of the traps
        for x in range((self.traps[0].posX-1), (self.traps[-1].posX), 2):
            for y in range(self.traps[0].posY, self.picking_cell[1], 2):
                self.graph.add_edge((x,y), (x+1,y-1), mid=(x,y-1), turn=1, weight=2, direction = 'straight')
                if y > 1:
                    self.graph.add_edge((x,y), (x,y-2), mid=(x,y-1), turn=0, weight=2, direction = 'straight')
            for y in range((self.picking_cell[1]+1), (self.traps[-1].posY+1), 2):
                self.graph.add_edge((x,y), (x+1,y+1), mid=(x,y+1), turn=1, weight=2, direction = 'straight')
                if y < self.traps[-1].posY:
                    self.graph.add_edge((x,y), (x,y+2), mid=(x,y+1), turn=0, weight=2, direction = 'straight')
        #edges departing from cells below the traps
        for x in range(self.traps[0].posX, (self.traps[-1].posX+1), 2):
            for y in range((self.traps[0].posY-1), (self.picking_cell[1]-1), 2):
                if y > 0:
                    self.graph.add_edge((x,y), (x+1,y-1), mid=(x+1,y), turn=1, weight=2, direction = 'straight')
                if x == self.traps[-1].posX: #if cell below most right trap
                    self.graph.add_edge((x,y), (x+2,y), mid=(x+1,y), turn=1, weight=2, direction = 'straight')
                else:
                    self.graph.add_edge((x,y), (x+2,y), mid=(x+1,y), turn=0, weight=2, direction = 'straight')
            for y in range((self.picking_cell[1]+2), (self.traps[-1].posY+1), 2):
                if y < self.traps[-1].posY:
                    self.graph.add_edge((x,y), (x+1,y+1), mid=(x+1,y), turn=1, weight=2, direction = 'straight')
                if x == self.traps[-1].posX:
                    self.graph.add_edge((x,y), (x+2,y), mid=(x+1,y), turn=1, weight=2, direction = 'straight')
                else:
                    self.graph.add_edge((x,y), (x+2,y), mid=(x+1,y), turn=0, weight=2, direction = 'straight')
            
        #special cells: cells from cells right to most-right traps to picking zone column
        for x in range ((self.traps[-1].posX+1), (self.traps[-1].posX+2), 2):
            for y in range (self.traps[0].posY, (self.picking_cell[1]-2), 2):
                self.graph.add_edge((x,y), (x+1,y), mid=0, turn=2, weight=1, direction = 'straight')
                self.graph.add_edge((x,y), (x+1,y-1), mid=(x,y-1), turn=2, weight=2, direction = 'straight')
            for y in range ((self.picking_cell[1]+1), (self.traps[-1].posY+1), 2):
                self.graph.add_edge((x,y), (x+1,y), mid=0, turn=2, weight=1, direction = 'straight')
                self.graph.add_edge((x,y), (x+1,y+1), mid=(x,y+1), turn=2, weight=2, direction = 'straight')

        #special cells: cells in the picking zone column
        x = self.picking_cell[0]
        for y in range ((self.traps[0].posY-1), self.picking_cell[1], 1):
            self.graph.add_edge((x,y), (x,y+1), mid=0, turn=0, weight=1, direction = 'straight')
        for y in range ((self.picking_cell[1]+1), (self.traps[-1].posY+2),1):
            self.graph.add_edge((x,y), (x,y-1), mid=0, turn=0, weight=1, direction = 'straight')
        #add edges to get out from chargers
        for charger in self.chargers:
            if charger.posY < self.picking_cell[1]:
                self.graph.add_edge((x+1,charger.posY), (x,charger.posY), mid=0, turn=1, weight=1, direction = 'left')
            else:
                self.graph.add_edge((x+1,charger.posY), (x,charger.posY), mid=0, turn=1, weight=1, direction = 'right')

    def weights_and_directions(self):
        #recalculate weights by taking turns into account
        # + provide the right direction
        for u, v in self.graph.edges():
            #recalculate weights
            self.graph[u][v]['weight'] = self.graph[u][v]['weight']/1.5 + (self.graph[u][v]['turn'])/2
            #provide the right direction
            if self.graph[u][v]['turn'] > 0 and self.graph[u][v]['mid']!=0:
                mid = self.graph[u][v]['mid']
                if (u[0]>mid[0] and mid[1]>v[1]) or (u[0]<mid[0] and mid[1]<v[1]) or (u[1]>mid[1] and mid[0]<v[0]) or (u[1]<mid[1] and mid[0]>v[0]):
                    self.graph[u][v].update(direction = 'right')
                elif (u[0]>mid[0] and mid[1]<v[1]) or (u[0]<mid[0] and mid[1]>v[1]) or (u[1]>mid[1] and mid[0]>v[0]) or (u[1]<mid[1] and mid[0]<v[0]):
                    self.graph[u][v].update(direction = 'left')
                else:
                    if u[1]>self.picking_cell[1]:
                        self.graph[u][v]['direction'] = 'left'
                    if u[1]<self.picking_cell[1]:
                        self.graph[u][v]['direction'] = 'right'
            elif self.graph[u][v]['turn'] > 0 and self.graph[u][v]['mid'] == 0:
                if u[0]>v[0]:
                    if u[1]<self.picking_cell[1]:
                        self.graph[u][v]['direction'] = 'left'
                    else:
                        self.graph[u][v]['direction'] = 'right'
                else:
                    if u[1]<self.picking_cell[1]:
                        self.graph[u][v]['direction'] = 'right'
                    else:
                        self.graph[u][v]['direction'] = 'left'

    def verify_overlap(self, a_depart, a_dest, b_depart, b_dest):
        #verify if robots are in each other's way
        late=0
        if a_depart<=b_dest and b_depart<=a_dest:
            late = b_dest - b_depart
        return (late)

    def verify_weight(self, robot_num, depart, dest, t_depart, t_dest):
        late=0
        a_traj=self.graph[depart][dest]['mid']
        for robot in self.warehouse.robotsManager.robots:
            if robot.port != robot_num and robot.time_path != None:
                temp_late = 0
                rtPath = robot.time_path
                #verify if robot stopped in the way(traps)
                if rtPath[-1][0] == dest:
                    temp_late = self.verify_overlap(t_depart, t_dest, rtPath[-1][1][0], rtPath[-1][1][1])
                    if temp_late > late:
                        late = temp_late
                if len(robot.time_path) > 1:
                    for x in range(1, len(rtPath)-1, 1):
                        b_traj= None
                        if robot.graph[rtPath[x][0][0]][rtPath[x][0][1]]['mid'] !=0:
                            b_traj = robot.graph[rtPath[x][0][0]][rtPath[x][0][1]]['mid']
                        #look for collisions between our robot and the others
                        if b_traj != None and b_traj == a_traj:
                            temp_late = 0
                            temp_late = self.verify_overlap(t_depart, t_dest, rtPath[x][1][0], rtPath[x][1][1])
                            if temp_late != 0:
                                #verify that robots' paths are not opposite (if one go up and the other down, they will be blocked)
                                if ((depart[0]-dest[0]>0 and rtPath[x][0][0][0]-rtPath[x][0][1][0]<0) or (depart[0]-dest[0]<0 and rtPath[x][0][0][0]-rtPath[x][0][1][0]>0)):
                                    if (depart[1]-dest[1]==0 and rtPath[x][0][0][1]-rtPath[x][0][1][1]==0):
                                        temp_late = 100
                                if ((depart[1]-dest[1]>0 and rtPath[x][0][0][1]-rtPath[x][0][1][1]<0) or (depart[1]-dest[1]<0 and rtPath[x][0][0][1]-rtPath[x][0][1][1]>0)):
                                    if (depart[0]-dest[0]==0 and rtPath[x][0][0][0]-rtPath[x][0][1][0]==0):
                                        temp_late = 100
                                if temp_late > late:
                                    late = temp_late
                                break
                        #make sure that robot don't break the queue for the picking zone
                        elif depart[0] < self.picking_cell[0] and dest[0] == self.picking_cell[0] and (rtPath[x][0][0] == dest or rtPath[x][0][1] == dest):
                            temp_late = 0
                            temp_late = self.verify_overlap(t_depart, t_dest, rtPath[x][1][0], rtPath[x][1][1])
                            if temp_late != 0:
                                temp_late = 100
                            if temp_late > late:
                                late = temp_late
        return (late)
                
                

    def get_shortest_path(self, graph=None, source=None, target=None, weight='weight', method='dijkstra'):
        path=nx.shortest_path(graph, source, target, weight, method)
        return(path)


    def choose_path(self, robot_num, graph_bis, source, target, t_current, max_late, times):
        #find shortest path between source and target
        path=self.get_shortest_path(graph_bis, source, target)
        t_depart=t_current
        tot_time=0 #time to make the shortest path (= sum of weights)
        reweighted_time = 0 #time to make the given shortest path, taking into account obstacles and collisions
        reweighted_graph = copy.deepcopy(graph_bis) #graph updated to take into account the found obstacles and collisions in the way
    	#for each part of the found path, look for obstacles or possible collisions with other robots
        for i in range(len(path)-1):
            t_dest = t_depart + self.graph[path[i]][path[i+1]]['weight']
            if self.graph[path[i]][path[i+1]]['mid'] != 0:
                late = self.verify_weight(robot_num, path[i], path[i+1], t_depart, t_dest)
            else:
                late = 0
            if late > 0:
                reweighted_graph[path[i]][path[i+1]]['weight'] += late
            tot_time += self.graph[path[i]][path[i+1]]['weight']
            reweighted_time += reweighted_graph[path[i]][path[i+1]]['weight']
            t_depart += reweighted_graph[path[i]][path[i+1]]['weight']
        tot_late = reweighted_time - tot_time
        end_path = []
        end_path.extend((path, reweighted_time, reweighted_graph))
        #calculate other paths if needed and choose for the shortest one in time
        if tot_late > max_late and times < 4:
            times +=1
            second_path = self.choose_path(robot_num, reweighted_graph, source, target, t_current, tot_late, times)
            if second_path[1] < reweighted_time:
                end_path = second_path
        return(end_path)


    def get_robot_path(self, robot_num, source, target, t_current):
        max_late = 2*.5
        #ask for shortest path taking into account robots and obstacles
        ret = self.choose_path(robot_num, self.graph, source, target, t_current, max_late, 0)
        #ret[0] = path; ret[1] = time of path, ret[2] = graph corresponding to path
        path = ret[0] #path useful for updating robot path (RobotsManager)
        graph = ret[2] #graph useful for updating robot path (RobotsManager)
        det_path=[] #detailed path for sending to the robot
        for x in range(len(path)-1):
            #add directions to detailed path for the robot
            part_path = self.graph[path[x]][path[x+1]]
            if part_path['turn'] > 0:
                if part_path['mid'] != 0:
                    if path[x][1] != path[x+1][1]:
                        det_path.append((part_path['mid'], part_path['direction']))
                    else:
                        det_path.append((part_path['mid'], 'straight'))
                elif path[x] < path[x+1]:
                    det_path[-1] = (path[x], part_path['direction'])
            if part_path['turn'] == 0 and part_path['mid'] != 0:
                det_path.append((part_path['mid'], 'straight'))
            if x < len(path)-2:
                det_path.append((path[x+1], 'straight'))
                if part_path['turn'] == 2 or (part_path['turn'] == 1 and path[x][1] == path[x+1][1]) or (path[x] > path[x+1]):
                    det_path[-1] = (path[x+1], part_path['direction'])
        inCharger = False
        for charger in self.chargers:
            if path[-1] == (charger.posX-1, charger.posY):
                det_path.append((path[-1], 'charge'))
                inCharger = True
                break
        if inCharger == False:
            if path[-1] == self.warehouse.picking_cell:
                det_path.append((path[-1], 'scan'))
            else:
                det_path.append((path[-1], 'drop'))
        return (det_path, path, graph)