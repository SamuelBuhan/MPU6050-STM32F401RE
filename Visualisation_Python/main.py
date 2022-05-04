# Created by Samuel BUHAN, 27/03/2022

from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5
from PyQt5.QtCore import Qt 
import pyqtgraph as pg
import serial as ps

class IMUVisualizer(QtWidgets.QWidget):
    """
    Visualize IMU data on PyQtgraph
    """
    nbData = 125
    all_accX = []
    all_accY = []
    all_accZ = []

    def __init__(self, steps=5, *args, **kwargs):
        super(IMUVisualizer, self).__init__(*args, **kwargs)
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.createWindow()
        try:
            self.serialPort = ps.Serial('COM3', 115200, timeout=0)
            self.serialPort.close()
            self.serialPort.open()
            if self.serialPort.isOpen():
                self.timer = QtCore.QTimer()
                self.timer.timeout.connect(self.readFrame)
                self.timer.start(10)
        except: 
            print("!COM port not found!")
            pass


    def createWindow(self):

        # tabs definition
        self.tabs = QtWidgets.QTabWidget()
        self.tabConfiguration = QtWidgets.QWidget()
        self.tabVisualise = QtWidgets.QWidget()


        self.tabs.addTab(self.tabVisualise,"Visualisation")
        self.tabs.addTab(self.tabConfiguration,"Configuration")
        

        # add tabs to main layout 
        self.mainLayout.addWidget(self.tabs)

        self.view = pg.GraphicsLayoutWidget()
        self.layoutGraphs = pg.GraphicsLayout(border=(100,100,100))


        # set visualise tab
        self.view.setCentralItem(self.layoutGraphs)

        self.plotItemAccX = self.layoutGraphs.addPlot(title="AccX")
        self.plotItemAccY = self.layoutGraphs.addPlot(title="AccY")
        self.plotItemAccZ = self.layoutGraphs.addPlot(title="AccZ")
        self.layoutGraphs.nextRow()

        self.plotItemGyroX = self.layoutGraphs.addPlot(title="GyroX")
        self.plotItemGyroY = self.layoutGraphs.addPlot(title="GyroY")
        self.plotItemGyroZ = self.layoutGraphs.addPlot(title="GyroZ")
        self.layoutGraphs.nextRow()

        self.plotItemMagnX = self.layoutGraphs.addPlot(title="MagnX")
        self.plotItemMagnY = self.layoutGraphs.addPlot(title="MagnY")
        self.plotItemMagnZ = self.layoutGraphs.addPlot(title="MagnZ")

        self.GraphAccX = self.plotItemAccX.plot()
        self.GraphAccY = self.plotItemAccY.plot()
        self.GraphAccZ = self.plotItemAccZ.plot()

        self.GraphAccX = self.plotItemGyroX.plot()
        self.GraphAccY = self.plotItemGyroY.plot()
        self.GraphAccZ = self.plotItemGyroZ.plot()

        self.GraphAccX = self.plotItemMagnX.plot()
        self.GraphAccY = self.plotItemMagnY.plot()
        self.GraphAccZ = self.plotItemMagnZ.plot()

        TmpLayout = QtWidgets.QHBoxLayout()
        TmpLayout.addWidget(self.view)
        self.tabVisualise.setLayout(TmpLayout)






        
        # self.view.show()
    def readFrame(self):
        if (self.serialPort.inWaiting()):
            frame = self.serialPort.read((self.serialPort.inWaiting()//self.nbData)*self.nbData)
            if frame == b'': return
            elif frame[0] == 0x55:
                # print("Frame:",frame.hex('-'),";len:",len(frame))
                for i in range(len(frame)//self.nbData):
                    # print("subFrame:",frame[self.nbData*i:self.nbData*(i+1)].hex('-'),";len:",len(frame[self.nbData*i:self.nbData*(i+1)]))
                    # print("Crc frame :",hex(frame[self.nbData*(i+1)-1]))
                    # print("Crc check :",hex(self.crcCheck(frame[self.nbData*i:self.nbData*(i+1)])))
                    if frame[self.nbData - 1] == self.crcCheck(frame[0:self.nbData]):
                        for j in range(10):
                            self.all_accX.append(frame[1+(j*2)] + (frame[2+(j*2)]<<8))

                self.GraphAccX.setData(self.all_accX)

    def crcCheck(self, frame):  
        crcValue = 0x00
        for i in range(0,len(frame)-1):
            crcValue = crcValue ^ frame[i]
        return crcValue

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    volume = IMUVisualizer()
    volume.show()
    app.exec_()