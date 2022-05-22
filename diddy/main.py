
import logging
import threading
import Diddy
import Connection
import Server_Order

if __name__ == '__main__':

    server_order = Server_Order.Server_Order()
    connection = Connection.Connection(server_order)
    diddy = Diddy.Diddy(connection, server_order)
    
    #Start the threading:
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main    : before creating thread")

    running_robot = threading.Thread(target = diddy.start)
    listen_server = threading.Thread(target = connection.wait_server_msg)
    

    logging.info("Main    : before running thread")
    listen_server.start()
    running_robot.start()
    logging.info("Main    : wait for the thread to finish")

    logging.info("Main    : all done")
        