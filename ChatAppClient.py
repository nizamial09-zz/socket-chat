from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox,QListWidget
from PyQt5.QtCore import pyqtSlot
import sys
import socket
from threading import Thread 
from socketserver import ThreadingMixIn 
import sys,time

client=None
class ChatApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(ChatApp, self).__init__()
        uic.loadUi('chatappclient.ui', self)
        self.message.returnPressed.connect(self.onClick)
        self.send1.clicked.connect(self.onClick)
    def onClick(self):
        msg=self.message.text()
        font=self.chatlist.font()
        font.setPointSize(13)
        self.chatlist.setFont(font)
        t='{:>80}'.format(msg)
        self.chatlist.append(t)
        client.send(msg.encode("utf-8"))
        self.message.clear()
        
class ClientThread(Thread):
    def __init__(self,win):
        Thread.__init__(self)
        self.win=win
    def run(self):
        host=socket.gethostname()
        port=8080
        SIZE=2000
        global client
        client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((host,port))
        while True:
            data=client.recv(SIZE)
            win.chatlist.append(data.decode("utf-8"))
        client.close()
if __name__=='__main__':


    app = QtWidgets.QApplication([])
    
    
    win = ChatApp()
    clientThread=ClientThread(win)
    clientThread.start()
    win.show()
    sys.exit(app.exec())