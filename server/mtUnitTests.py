#import unittest
import mt
import queue
import _thread
import time
class DummySocket:

    def __init__(self, ID):
        self.id = ID
        self.lastMsg = ""
    
    def send(self, msg):
        print(self.id+":",msg)
        self.lastMsg = msg

    def close(self):
        print(self.id+": CLOSE CALLED")
        self.lastMsg = "CLOSED"

    def getpeername(self):
        return self.id, 0
    
##class TestMt(unittest.TestCase):
##
##    def test_listener_thread(self):
##        data = queue.Queue()
##        s1 = DummySocket("0")
##        s2 = DummySocket("1")
##
##        listenerObj = mt.ListenerThread(data)
##        
##        def sender():
##            time.sleep(1)
##            data.put("Hello, World")
##            time.sleep(0.1)
##            listenerObj.add(s2)
##            time.sleep(1)
##            data.put("Hello, World 2")
##            time.sleep(1)
##            listenerObj.removeIP("0")
##            data.put("Hello, World 3")
##            
##            data.put("!!INTERNAL=SHUTDOWN!!")
##
##        listenerObj.add(s1)
##        _thread.start_new_thread(sender, ())
##        listenerObj.main()
##
##        self.assertEqual(s1.lastMsg, "CLOSED")
##        self.assertEqual(s2.lastMsg, b"Hello, World 3\r\n")


def test_listener_thread(self):
            data = queue.Queue()
        s1 = DummySocket("0")
        s2 = DummySocket("1")

        listenerObj = mt.ListenerThread(data)
        
        def sender():
            time.sleep(1)
            data.put("Hello, World")
            time.sleep(0.1)
            listenerObj.add(s2)
            time.sleep(1)
            data.put("Hello, World 2")
            time.sleep(1)
            listenerObj.removeIP("0")
            data.put("Hello, World 3")
            
            data.put("!!INTERNAL=SHUTDOWN!!")

        listenerObj.add(s1)
        _thread.start_new_thread(sender, ())
        listenerObj.main()

        assert s1.lastMsg == "CLOSED")
        assert s2.lastMsg == b"Hello, World 3\r\n")

                
        
        
    
