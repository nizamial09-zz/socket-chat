from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox,QListWidget,QApplication
from PyQt5.QtCore import pyqtSlot
import sys
import socket
from threading import Thread 
from socketserver import ThreadingMixIn 
import sys,time

conn=None
class ChatApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(ChatApp, self).__init__()
        uic.loadUi('chatapp.ui', self)
        self.message.returnPressed.connect(self.onClick)
        self.send1.clicked.connect(self.onClick)
    def onClick(self):
        msg=self.message.text()
        font=self.chatlist.font()
        font.setPointSize(13)
        self.chatlist.setFont(font)
        t='{:>80}'.format(msg)
        self.chatlist.append(t)
        
        conn.send(msg.encode("utf-8"))
        self.message.clear()
        
class ServerThread(Thread):
    def __init__(self,win):
        Thread.__init__(self)
        self.win=win
    
    def run(self):
        IP='0.0.0.0'
        PORT=8080
        SIZE=2000
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server.bind((IP,PORT))
        threads=[]
        server.listen(4)
        while True:
            print("Multithreaded Python server : Waiting for connections from TCP clients...") 
            global conn
            (conn,(ip,port))=server.accept()
            new=ClientThread(ip,port,win)
            new.start()
            threads.append(new)
        for t in threads:
            t.join()
class ClientThread(Thread):
    def __init__(self,ip,port,win):
        Thread.__init__(self)
        self.win=win
        self.ip=ip
        self.port=port
        print("[+] New server socket thread started for " + ip + ":" + str(port))
    def run(self):
        while True:
            data=conn.recv(2048)
            win.chatlist.append(data.decode("utf-8"))
            print(data)
if __name__=='__main__':


    app = QtWidgets.QApplication([])
    
    
    win = ChatApp()
    serverThread=ServerThread(win)
    serverThread.start()
    win.show()
    sys.exit(app.exec())