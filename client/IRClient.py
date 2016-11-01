import socket, _thread, tkinter as tk, tkinter.ttk as ttk
from time import strftime, sleep
from tkinter import messagebox, simpledialog

#===========================================================================#

class BasicInputDialog:
    def __init__(self,question,title=None,hideWindow=True):
        if title == None:
            title = PROGRAM_TITLE
        self.master = tk.Tk()
        self.string = ''
        self.master.title(title)
        self.frame = tk.Frame(self.master)
        self.frame.pack()        
        self.acceptInput(question)
        self.waitForInput()
        try:
            self.inputted = self.getText()
        except Exception:
            quit()
        
    def acceptInput(self,question):
        r = self.frame
        k = ttk.Label(r,text=question)
        k.grid(row=0,column=0)
        self.e = ttk.Entry(r,width=30)
        self.e.grid(row=1,columnspan=2)
        self.e.focus_set()
        b = ttk.Button(r,text='Enter',command=self.getText)
        self.master.bind("<Return>", self.getText)
        b.grid(row=0,column=1,padx=5,pady=5)

    def getText(self,event=None):
        self.string = self.e.get()
        self.master.quit()
        return self.string

    def get(self):
        self.master.destroy()
        return self.inputted

    def getString(self):
        return self.string

    def waitForInput(self):
        self.master.mainloop()

#Main window application
class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title(PROGRAM_TITLE)
        self.resizable(0,0)

        self.displayBox = tk.Text(self, width=100, font=THEME.font, bg=THEME.colors[3], fg=THEME.colors[0])
        self.displayBox.pack()
        self.displayBox.configure(state='disabled')
        
        self.msgEntry = tk.Entry(self,width=100, font=THEME.font, bg=THEME.colors[3], fg=THEME.colors[1], insertbackground = THEME.colors[2])
        self.msgEntry.pack()

        self.bind("<Return>", self.sendText)
        
    def sendText(self,event=None):
        send(newMessage(self.msgEntry.get()).toString())
        self.msgEntry.delete(0, 'end')

class Theme:
    def __init__(self, font, colors):
        self.colors = colors #Message,input,cursor,background
        self.font = font

class Message:
    #Static variables for formatting
    sep = "§"
    pref = "msg="
    SUDO_PREF = "server="

    #Initiate, if timestamp is not entered it will be current time
    def __init__(self, sender, plainText, timestamp = None):
        if timestamp == None:
            timestamp = strftime("%d-%m-%Y %H:%M:%S")

        self.plainText = plainText
        self.sender = sender
        self.timestamp = timestamp

    #Sends to string object to be sent through socket
    def toString(self):
        return self.pref + self.sender + self.sep + self.timestamp + self.sep + self.plainText

    #Turns recieved strings into messages: returns None if invalid.
    def fromString(text):
        if not text.startswith(Message.pref):
            return Message("SERVER",text[len(Message.SUDO_PREF):]) if text.startswith(Message.SUDO_PREF) else None
        data = text[len(Message.pref):].split(Message.sep,2)
        return Message(data[0],data[2],data[1])

    #Converts into display string
    def toFormattedString(self):
        return "["+self.timestamp + "] <" + self.sender + ">: "+self.plainText

#===========================================================================#
        
def send(msg):
    try:
        SEND_SOCKET.send(bytes(msg,'UTF-8'))
    except:
        print("Unable to send message")

def newMessage(msg):
    return Message(NICKNAME, msg)

def waitForMessages(s,window):
    #This should be run in a seperate thread: constantly recieves new messages
    sleep(0.5)
    while True:
        #Recieve message and convert to string
        msg = s.recv(1024)
        msg = str(msg, "UTF-8")

        #Checking if message follows Message class format
        m = Message.fromString(msg)

        if m == None: continue

        msg = m.toFormattedString()

        #Show in window
        writeTo(window.displayBox,msg)

def writeTo(textBox,msg):
    textBox.configure(state='normal')
    textBox.insert('end',msg)
    textBox.configure(state='disabled')
    textBox.see(tk.END)

def shutdownHook():
    send("!DISCONNECT")
    root.destroy()
    quit()

#===========================================================================#  
PROGRAM_TITLE = 'TG\'s IRC'
SERVER_IP = input("Enter IP:").strip()
NICKNAME = BasicInputDialog("Enter Nickname:").get()
THEME = Theme(("Consolas", 10), ['green', 'cyan', 'white', 'black'])


RECV_SOCKET = socket.socket()
RECV_SOCKET.connect((SERVER_IP, 20075))

SEND_SOCKET = socket.socket()
SEND_SOCKET.connect((SERVER_IP, 20074))
send("!nickname="+NICKNAME)

root = MainWindow()
_thread.start_new_thread(waitForMessages, (RECV_SOCKET,root,))
root.protocol("WM_DELETE_WINDOW", shutdownHook)
root.mainloop()
