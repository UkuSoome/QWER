class RefHandler:


    def __init__(self,RobotID, FieldID,mb):
        self.robotID = RobotID
        self.fieldID = FieldID
        self.mb = mb


    def setRobotID(self,RobotID):
        self.robotID = RobotID

    def setFieldID(self,FieldID):
        self.fieldID = FieldID

    def handleMsg(self,msg):
        cmd = ""
        if msg[0] == "a":
            if msg[1] == self.fieldID:
                if msg[2] == self.robotID or msg[2] == "X":
                    if msg[2] == self.robotID:
                        self.sendAck()
                    endOfMsg = msg.find("-")
                    if endOfMsg != -1:
                        cmd = msg[3:endOfMsg]
                    else:
                        cmd = msg[3:].strip()
        return cmd

    def sendAck(self):
        self.mb.sendBytes("rf:a" + self.fieldID + self.robotID + "ACK------")