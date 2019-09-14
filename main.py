from gameLogic import GameLogic
from imageProccessing import ImageProcessing
import threading



imageHandler = ImageProcessing.ImageProccessing()
gameHandler = GameLogic.GameLogic(imageHandler)

imageThread = threading.Thread(target=imageHandler.run)
imageThread.start()

gameThread = threading.Thread(target=gameHandler.run)
gameThread.start()