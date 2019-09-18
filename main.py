from gameLogic import GameLogic
from imageProccessing import ImageProcessing
from mainboardCommunication import MainboardCommunication
from imageProccessing import thresholding
import threading
import time


mainComm = MainboardCommunication.MainboardCommunication()

imageHandler = ImageProcessing.ImageProccessing(mainComm)

gameHandler = GameLogic.GameLogic(imageHandler, mainComm)

imageThread = threading.Thread(target=imageHandler.run)
imageThread.start()
time.sleep(2)

gameThread = threading.Thread(target=gameHandler.run)
gameThread.start()
