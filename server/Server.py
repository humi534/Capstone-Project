import socket
import threading
import time
import json
import Manager


HEADER = 16
PORT = 5050
#SERVER = "127.0.0.1" 
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

class Server:
    def __init__(self) -> None:
        self.manager = Manager.Manager()
        self.warehouse = self.manager.warehouse
        self.A = self.manager.A
        self.R = self.manager.R
        self.P = self.manager.P

        #self.warehouse.packagesManager.change_still_products()
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock = threading.Lock()

        try:
            self.server.bind(ADDR)
        except socket.error:
            print("Bind failed")

    def start(self):
        print("[STARTING] server is starting ...")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        num_robot = threading.active_count() - 1
        self.warehouse.robotsManager.add_robot(num_robot, addr[1], None, None)

        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg_received = conn.recv(msg_length).decode(FORMAT)

                print("receiving:", f"[{addr}] {msg_received}")
                time.sleep(2)
                if msg_received == DISCONNECT_MESSAGE:
                    connected = False

                else:
                    self.lock.acquire()
                    self.handle_client_response(conn, msg_received)
                    self.lock.release()
        #conn.close()

    def send_and_save_path(self, conn, robot_id, source, target, graph):
        #compute the path
        path = graph.get_robot_path(robot_id, source, target, time.time())
        #return the path
        return_msg = json.dumps({"path": path[0]})
        self.send(conn, return_msg)
        #update the path for the robot
        self.warehouse.robotsManager.write_robots_path(robot_id, path[2], path[1], self.warehouse.picking_cell, time.time())
        #print(self.warehouse.robotsManager.robots[0].time_path)

    def handle_client_response(self, conn, msg):
        try:
            msg = json.loads(msg)
        except:
            print("json not able to be converted")
            
        graph = None
        source = None
        target = None

        robot_id = msg["id"]
        
        #if the robot is AVAILABLE
        if "msg" in msg and msg["msg"] == "AVAILABLE":
            #get the robot
            robot = self.warehouse.robotsManager.get_robot_by_id(robot_id)
            if robot:
                graph = self.R
                source = robot.time_path[0][0]
                target = self.warehouse.picking_cell
                #send the path to the robot and save it into the server
                print("source: ", source, ", target: ", target)
                self.send_and_save_path(conn, robot_id, source, target, graph)
            
        #si robot a besoin d'un path
        elif "product delivered" in msg:
            
            #remove package
            product_id = msg["product_id"]
            #add the parcel into the delivered package list
            self.warehouse.packagesManager.add_delivered_package(product_id)

            still_product = self.warehouse.packagesManager.get_still_products()
            robot = self.warehouse.robotsManager.get_robot_by_id(robot_id)

            #check if we still have parcels
            if still_product and robot:
                graph = self.R
                source = robot.time_path[-1][0]
                target = self.warehouse.picking_cell
                self.send_and_save_path(conn, robot_id, source, target, graph)
            else:
                #envoyer à charger car plus de produits
                wait = json.dumps({"msg": 'wait'})
                self.send(conn, wait)
        
        elif "target" in msg:

            source = self.warehouse.picking_cell
            target = (msg["target"][0],msg["target"][1])
            graph = self.A
            product_id = msg["product_id"]

            #add the parcel into the moving package list
            self.warehouse.packagesManager.add_moving_package(product_id)
            #compute the path
            self.send_and_save_path(conn, robot_id, source, target, graph)
            
        elif "pos" in msg:
            position = (msg["pos"][0],msg["pos"][1])
            pos_time = msg["pos_time"]
            #update the robot's path
            good_path = self.warehouse.robotsManager.check_robots_position(robot_id, position, pos_time) #check if it's the good path, else update the robot position

            if not good_path:
                wait = json.dumps({"msg": 'wait'})
                self.send(conn, wait)
            
                robot = self.warehouse.robotsManager.get_robot_by_id(robot_id)
                if robot:
                    graph = self.P #problem(s) --> graph (if path needs to be recalculated)
                    source = position
                    target = robot.time_path[-1][0]
                    self.send_and_save_path(conn, robot_id, source, target, graph)

        else:
            self.send(conn, "Disconnect!")
        #self.lock.release()

    def send(self, conn, msg:str):
        print("sending: ", msg)
        time.sleep(2)
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)



server = Server()
server.start()