from gameLogic import GameLogic
from imageProccessing import ImageProcessing
from mainboardCommunication import MainboardCommunication
import threading
from wheelMovementLogic import WheelMovementLogic


wheelLogic = WheelMovementLogic.WheelMovementLogic()

imageHandler = ImageProcessing.ImageProccessing()
mainComm = MainboardCommunication.MainboardCommunication('/dev/ttyACM0',imageHandler)
gameHandler = GameLogic.GameLogic(imageHandler, mainComm)

imageThread = threading.Thread(target=imageHandler.run)
imageThread.start()


gameThread = threading.Thread(target=gameHandler.run)
gameThread.start()

