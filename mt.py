import queue
import socket
import threading
import re
import resources as r
import random

####CONSTANTS####
ENCODING = 'UTF-8'
RECV_PORT = 20074
SEND_PORT = 20075
MAX_CONN = 5

####CLASSES####
class ListenerThread:

    def __init__(self, data):
        self.connections = []

        self.lock = threading.Lock()
        self.data = data
        self.numconn = 0
        
    #Called when a new connections occurs on the main thread, adds a new socket
    #object to the queue to send new messages to
    def add(self, socket):
        success = False
        with self.lock:
            if self.numconn != MAX_CONN or MAX_CONN == 0:
                self.connections.append(socket)
                self.numconn += 1
                socket.send(random.choice(r.allCredits))
                success = True
        return success

            

    #Called whenever a new message is receved, also disconnects any inactive
    #sockets
    def send(self, data):
        with self.lock:
            for conn in self.connections:
                try:
                    conn.send(bytes(data+'\r\n',ENCODING))
                except OSError:
                    self.connections.remove(conn)
                    self.numconn -= 1

    #Main code to be run in a seperate thread
    def main(self):
        while True:
            data = self.data.get()
            self.send(data)

#RecvManager to handle the creation of new threads to manage input from clients
class RecvManager:

    def __init__(self, data, maxconnections = 0):
        self.data = data
        self.maxconnections = maxconnections

    def main(self):
        s = socket.socket()
        s.bind(("",RECV_PORT))
        s.listen(self.maxconnections)
        while True:
            c, addr = s.accept()
            recvObj = RecvThread(self.data, c)
            recvThread = threading.Thread(target=recvObj.main)
            recvThread.start()

#RecvThread, created by RecvManager to serve a specific client          
class RecvThread:

    def __init__(self, data, s):
        self.data = data
        self.s = s
        self.nickname = "LEGACY/UNSUPPORTED CLIENT"
        
    def main(self):
        while True:
            try:
                msg = re.sub('\n', ' ', str(self.s.recv(1024), ENCODING))
                print("RECV:",msg)
            except:
                self.disconnectHandler(False)
            self.cmdParser(msg)

    def cmdParser(self, msg):
        if msg.startswith("!nickname="):
            self.nicknameManager(msg[10:])
        elif msg.startswith("!DISCONNECT"):
            self.disconnectHandler()
        else:
            self.data.put(msg)
            
    def nicknameManager(self, nickname):
        if self.nickname == "LEGACY/UNSUPPORTED CLIENT":
            self.data.put(r.joinMsg.format(nickname))
        else:
            self.data.put(r.nickChangeMsg.format(self.nickname,nickname))
        #END IF BLOCK#
        self.nickname = nickname
        
    def disconnectHandler(self, safe=True):
        if safe:
            self.data.put(r.leaveMsg.format(self.nickname))
            self.s.close()
            quit()
        else:
            self.data.put(r.unsafeLeaveMsg.format(self.nickname))
            quit()

#Main Code Block, sets everything up and also manages listening for new clients
def main():
    data = queue.Queue()
    listenerObject = ListenerThread(data)
    listenerThread = threading.Thread(target=listenerObject.main)
    listenerThread.start()
    recvObj = RecvManager(data)
    recvThread = threading.Thread(target=recvObj.main)
    recvThread.start()
    s = socket.socket()
    s.bind(("",SEND_PORT))
    s.listen(5)
    print(random.choice(r.allStart))
    while True:
        c, addr = s.accept()
        success = listenerObject.add(c)
        if not success:
            c.send(bytes("ERROR: SERVER IS FULL",'UTF-8'))
            c.close()

if __name__ == '__main__':
    main()
