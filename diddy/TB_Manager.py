import ThunderBorg3 as ThunderBorg
import time

class TB_Manager:
    def __init__(self) -> None:
        print("start motors")
        """
        self.TB = ThunderBorg.ThunderBorg()
        #TB.i2cAddress = 0x15                  # Uncomment and change the value if you have changed the board address
        self.TB.Init()"""
    
    def move(self, direction) -> None:
        print("move " + direction)
        """
        drive_left = 0.0
        drive_right = 0.0

        if direction =="left": #0.27 if straight before, 0.29 if not moving before
            drive_left = -0.27
            drive_right = +0.27
        elif direction == "right": #0.27 if straight before, 0.29 if not moving before
            drive_left = +0.27
            drive_right = -0.27
        elif direction == "straight":
            drive_left = +0.5
            drive_right = +0.5    
        self.TB.SetMotor1(drive_left)
        self.TB.SetMotor2(drive_right)
        time.sleep(0.5)
        self.TB.MotorsOff()
        """

    #Attention à tester pr faire 90 degré (0.534 pour 90 degrés piles pleines)
    def turn_left(self) -> None:
        print("left")
        """
        drive_left = -0.534
        drive_right = +0.534
        self.TB.SetMotor1(drive_left)
        self.TB.SetMotor2(drive_right)
        time.sleep(0.5)
        self.TB.MotorsOff()
        """

    #Attention à tester pr faire 90 degré (0.538 pour 90 degrés piles pleines)
    def turn_right(self) -> None:
        print("right")
        """
        drive_left = +0.538
        drive_right = -0.538
        self.TB.SetMotor1(drive_left)
        self.TB.SetMotor2(drive_right)
        time.sleep(0.5)
        self.TB.MotorsOff()
        """

    def stop(self) -> None:
        print("motor off")
        #time.sleep(0.5)
        #self.TB.MotorsOff()
    
    