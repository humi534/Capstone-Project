from Robot import Robot
#from ChargersManager import ChargersManager

class RobotsManager:
    
    def __init__(self) -> None:
        self.robots = []
        
    def add_robot(self, num, port, time_path, graph):
        self.robots.append(Robot(num, port, time_path, graph))
    
    def get_robot_by_id(self, id) -> Robot:
        for robot in self.robots:
            if robot.id == id:
                return robot
        return None

    def get_robot_by_port(self, port) -> Robot:
        for robot in self.robots:
            if robot.port == port:
                return robot  
        return None

    def get_robots_data(self) -> dict:
        """
        example:
        robots_dict = {1:{'posX':10, 'posY':5, 'direction':'south', 'batteryLevel':55}}
        """
        robots_dict = {}
        for robot in self.robots:
            robots_dict[robot.id] = {"posX":robot.posX, "posY":self.posY, "direction":robot.direction, "batteryLevel":robot.batteryLevel}

        return robots_dict
    
    def write_robots_path(self, id, graph, path, picking_cell, t_depart):
        robot = self.get_robot_by_id(id) #choose right robot depending on the port
        if robot:
            robot.time_path.clear()
            robot.graph = graph #keep graph corresponding to the robots path
            #keep each part of robot path + time to do the path (start time and end time)
            for i in range(len(path)-1):
                t_dest = t_depart + graph[path[i]][path[i+1]]['weight']
                if path[i][0] == picking_cell[0] and path[i+1][0] == picking_cell[0]:
                    #recalculate time of robot in the picking queue, depending on other robots in front of him
                    t_dest = self.update_robots_queue_time(robot, graph, path[i], path[i+1], t_depart, t_dest)
                robot.time_path.append([[path[i], path[i+1]], [t_depart, t_dest]])
                t_depart = t_dest
            #keep at the end the last point with an estimated time that the robot will take there
            robot.time_path.append([path[-1], [t_depart, t_depart+3]])
                
                
    def update_robots_queue_time(self, my_robot, graph, depart, dest, t_depart, t_dest):     
        checked = False
        for robot in self.robots:
            if robot.time_path != None and len(robot.time_path) > 1:
                for x in range(len(robot.time_path)):
                    #update time that robot will take in the picking zone queue
                    if robot.time_path[x][0][0] == dest:
                        #check for overlapping
                        if t_depart<=robot.time_path[x][1][1] and robot.time_path[x][1][0]<=t_dest:
                            #update for our robot
                            t_dest += graph[my_robot.time_path[x][0][0]][my_robot.time_path[x][0][1]]['weight']
                            checked = True
                            break
                else:
                    continue
            if checked == False:
                break
        return t_dest
        
        
    def check_robots_position(self, id, current_pos, pos_time):
        good_path = False
        robot = self.get_robot_by_id(id) #choose right robot depending on the port
        if robot:
            for i in range(len(robot.time_path)):
                #check if robot position is in its path (if position = real pos or last path pos)
                if i < len(robot.time_path)-1 and robot.time_path[i][0][0] == current_pos or robot.time_path[i][0] == current_pos:
                    good_path = True
                    saved_time = robot.time_path[0][1][0]
                    self.update_robots_path = (robot, i, pos_time, saved_time) #update path
                    break
                #check if robot position is in its path (if position = mid pos)
                elif i < len(robot.time_path)-1 and robot.graph[robot.time_path[i][0][0]][robot.time_path[i][0][1]]['mid'] == current_pos:
                    good_path = True
                    robot_pos = robot.graph[robot.time_path[0][0][0]][robot.time_path[0][0][1]]
                    mid_time = (robot_pos['weight'] - robot_pos['turn'])/2
                    saved_time = robot.time_path[i][1][0] + mid_time
                    self.update_robots_path = (robot, i, pos_time, saved_time) #update path
                    break
        return good_path


    def update_robots_path(self, robot, i, pos_time, saved_time):
        #delete already visited paths
        for j in range(i):
            robot.time_path.pop(0)
        diff_time = pos_time - saved_time #verify if robot took more/less time than expected
        if diff_time != 0:
            #add time difference to next expected times
            for k in range(len(robot.time_path)):
                for l in range(len(robot.time_path[k][1])):
                    robot.time_path[k][1][l] += diff_time
        