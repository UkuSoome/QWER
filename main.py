from gameLogic import GameLogic
from imageProccessing import ImageProcessing
from mainboardCommunication import MainboardCommunication
import threading
import time
from wheelMovementLogic import WheelMovementLogic


wheelLogic = WheelMovementLogic.WheelMovementLogic()


mainComm = MainboardCommunication.MainboardCommunication()

imageHandler = ImageProcessing.ImageProccessing(mainComm)

gameHandler = GameLogic.GameLogic(imageHandler, mainComm)

imageThread = threading.Thread(target=imageHandler.run)
imageThread.start()


gameThread = threading.Thread(target=gameHandler.run)
gameThread.start()
