
# import the necessary packages
from picamera import PiCamera
from realsense_depth import DepthCamera
import time
from pyzbar import pyzbar
import cv2
import json
import numpy as np
#import pyrealsense2
import TB_Manager
import sys
import traceback
import warnings
import logging

warnings.filterwarnings("ignore")
BLUE = (255,0,0)
GREEN = (0,255,0)

class Diddy:
    def __init__(self, connection, server_order) -> None:
        
        self.id = 1
        self.server_order = server_order
        self.conn = connection

        #Setup the cameras
        self.dc = DepthCamera()
        self.piCamera = PiCamera()

        self.running = False

        #Setup the motor
        self.thunderborg = TB_Manager.TB_Manager()

        self.last_scanned_data = None
        self.path_robot = []
        self.current_position = []
        self.current_product = None
        self.is_waiting_parcel = False
        self.send({"msg":"AVAILABLE"})
        self.action = None

    def update_path(self, newPath) -> None:
        self.path = newPath

    def check_if_new_data(self, data:dict) -> bool:
        return data != self.last_scanned_data and data != None
 
    def center_red_detection(self, frame) -> int:
        """Return the mean of the red points given a frame"""
        # define the list of boundaries
        #boundary = [[17, 15, 100], [50, 56, 200]]
        boundary = [[17, 15, 95], [60, 66, 230]]
        # loop over the boundaries
        lower = boundary[0]
        upper = boundary[1]
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        # find the colors within the specified boundaries and apply the mask
        mask = cv2.inRange(frame, lower, upper)
        #red_only = cv2.bitwise_and(image, image, mask = mask)
        x_indexes = []

        for y in range(len(mask)):
            for x in range(len(mask[0])):
                if mask[y][x]:
                    x_indexes.append(x)

        try:
            return int(np.mean(x_indexes))
        except:
            return 324

    def barcode(self, image) -> str:
        """Return the data from the barcode based on the image given"""
        barcodes = pyzbar.decode(image)
        data = None
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            print("-------------------------Detect------------------------")
            print(data)
            barcode_info = barcode.data.decode('utf-8')
            data = json.loads(barcode_info)
        return data

    def take_picture(self):
        image_name = 'image.jpg'
        self.piCamera.capture('/home/pi/Desktop/Final/Connectionpy/%s' % image_name)
        image = cv2.imread(image_name)
        return image

    def line_tracker(self, frame) -> None:
        """Red line tracker"""
        mean = self.center_red_detection(frame)
        if mean == np.nan:
            mean = 324
        left_threshold = 200
        right_threshold = 450
        if mean >= right_threshold:
            print ("Turn Right!")
            self.thunderborg.move("right")
        elif mean >= left_threshold:
            print ("Turn Left")
            self.thunderborg.move("left")
        else: #mean < right_threshold and mean > left_threshold:
            print ("On Track!")
            self.thunderborg.move("straight")
            
        #Show the frame with the red line tracker
        """line_thickness = 2
        cv2.line(frame,(mean,0),(mean,848),BLUE,line_thickness)
        cv2.line(frame,(left_threshold,0),(left_threshold,848),GREEN,line_thickness)
        cv2.line(frame,(right_threshold,0),(right_threshold,848),GREEN,line_thickness)
        cv2.imshow("images", np.hstack([frame]))"""
    
    def update_position(self, data) -> None:
        if data["is_product"] == False:
            self.current_position = data["pos"]
            
    def send_position(self) -> None:
        self.send({"pos":self.current_position, "pos_time":time.time()})

    def send(self, msg:dict) -> None:
        """Send a dictionnary to the server including the id of the robot and the message"""
        msg_to_send = {'id':self.id}
        msg_to_send.update(msg)
        self.conn.send(msg_to_send)

    def check_path(self) -> bool:
        """
        Return True if current_position is in path and update path
        Return False otherwise
        """
        for i in range(len(self.path_robot)):
            if self.current_position == self.path_robot[i][0]:
                self.action = self.path_robot[i][1]
                del self.path_robot[:i+1]
                return True
        return False

    def check_action(self) -> None:
        """Check the path to know the next action"""
        #the path_robot[0] value is the futur position
        print("action ", self.action)
        if self.action == 'left':
            print("Turn left here to continue your path")
            self.thunderborg.turn_left()
            #self.thunderborg.move()
        if self.action == 'right':
            print("Turn right here to continue your path")
            self.thunderborg.turn_right()
            #self.thunderborg.move()
        if self.action == 'scan':
            self.wait_parcel()

    def destination_reached(self) -> bool:
        return len(self.path_robot) == 0

    def drop_parcel(self, data:dict) -> bool:
        print("Drop the parcel")
        self.thunderborg.stop()
        self.send({"product":data["produit"], "is_delivered": 'true'})

    def wait_server_order(self):
        """Stop Diddy and wait for an order of the server"""
        print("wait for a message")
        self.running = False
        self.thunderborg.stop()
        while True:
            if self.server_order.get_has_been_modified():
                server_msg = self.server_order.get_msg()
                self.decrypt(server_msg)

    def decrypt(self, msg):
        """Analyse the order given by the server"""
        #if the msg contains a path
        if "path" in msg:
            self.path_robot.clear()
            self.path_robot = msg["path"]
            print("path ", self.path_robot)
            self.running = True
            self.main()

        #if the msg contains "wait"
        if "msg" in msg and msg["msg"] == "wait":
            self.wait_server_order()

        #if the robot is at the picking zone and have to scan a parcel  
        if "scan" in msg:
            self.wait_parcel()

    def wait_parcel(self)-> None:
        data = None
        while True:
            image = self.take_picture()
            data = self.barcode(image)
            if data and data["is_product"]:

                #send information about product 
                print("New product to move at", data["pos"])
                self.current_product = data["produit"]
                self.send({"target":data["pos"], "product":data["produit"]})

                #wait for response
                self.wait_server_order()
        
    def start(self)-> None:
        self.wait_server_order()
        
    def main(self) -> None:
        logging.info("Thread Diddy main: starting")
        try:
            print('Press CTRL+C to quit')
            while self.running:

                # Capture the frames
                ret, depth_frame, frame = self.dc.get_frame()
                self.line_tracker(frame)

                #Search a barcode
                image = self.take_picture()
                data = self.barcode(image)
                print("data scanned: ", data)
                
                
                if self.check_if_new_data(data):
                    self.last_scanned_data = data
                    self.update_position(data)
                    print("new position ", self.current_position)
                    checked_path = self.check_path()
                    #Check if the robot is on the right pat
                    if not checked_path and self.action != "scan" :
                        self.send({"changepath":'change path', "pos":self.current_position,"pos_time":time.time()})
                        self.running = False
                        self.wait_server_order()

                    else:
                        #Send informations about the new position
                        self.send_position()
                        self.check_action()
                        

                    #Drop the parcel if needed and wait new path from the server
                    if self.destination_reached():
                        self.drop_parcel(data)
                        self.send({"prod_num": self.current_product, "product delivered":"product delivered"})
                        self.current_product = None
                        self.running = False
                        self.wait_server_order()

                #Turn
                #self.check_action()

        except KeyboardInterrupt:
        # CTRL+C exit, disable all drives
            print ('User shutdown')
            self.running = False
            self.thunderborg.stop()
            
        except:
            # Unexpected error, shut down!
            e = sys.exc_info()[0]
            print(e)
            traceback.print_exc()
            print ('Unexpected error, shutting down!')
            self.thunderborg.stop()
        # Tell each thread to stop, and wait for them to end
        self.running = False
        self.thunderborg.stop()
        print ('Program terminated.')

        logging.info("Thread Running Robot: finishing")
        
