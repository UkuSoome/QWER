from gameLogic import GameLogic
from imageProccessing import ImageProcessing
from mainboardCommunication import MainboardCommunication
import threading
from wheelMovementLogic import WheelMovementLogic


wheelLogic = WheelMovementLogic.WheelMovementLogic()


mainComm = MainboardCommunication.MainboardCommunication('/dev/ttyACM0')

imageHandler = ImageProcessing.ImageProccessing(mainComm)

gameHandler = GameLogic.GameLogic(imageHandler, mainComm)

imageThread = threading.Thread(target=imageHandler.run)
imageThread.start()


gameThread = threading.Thread(target=gameHandler.run)
gameThread.start()
