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
    nbData = 14 # number of data per frame

    # accelerometer sensitivity scale factor corresponding to {2g,4g,8g,16g}
    accSensScaleFactor = {"2g":16384, 
                          "4g" :8192,
                          "8g" : 4096,
                          "16g" : 2048}
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
                self.timer.start(1)
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

        # set limits 
        self.plotItemAccX.setYRange(-2,2)
        self.plotItemAccY.setYRange(-2,2)
        self.plotItemAccZ.setYRange(-2,2)

        self.GraphAccX = self.plotItemAccX.plot()
        self.GraphAccY = self.plotItemAccY.plot()
        self.GraphAccZ = self.plotItemAccZ.plot()

        self.GraphGyroX = self.plotItemGyroX.plot()
        self.GraphGyroY = self.plotItemGyroY.plot()
        self.GraphGyroZ = self.plotItemGyroZ.plot()

        self.GraphMagnX = self.plotItemMagnX.plot()
        self.GraphMagnY = self.plotItemMagnY.plot()
        self.GraphMagnZ = self.plotItemMagnZ.plot()

        TmpLayout = QtWidgets.QHBoxLayout()
        TmpLayout.addWidget(self.view)
        self.tabVisualise.setLayout(TmpLayout)


        



        
        # self.view.show()
    def readFrame(self):
        if (self.serialPort.inWaiting()):
            frame = self.serialPort.read(self.nbData)
            if frame == b'': return
            elif frame[0] == 0x55:
                # print("Frame:",frame,";len:",len(frame))
                # print("Frame:",frame.hex('-'),";len:",len(frame))
                # print("CrcFrame:",hex(frame[self.nbData - 1]))
                # print("subFrame:",frame[0:self.nbData - 1].hex('-'))
                # print("CrcSubFrame:",hex(self.crcCheck(frame[0:self.nbData])))
                # print('-' * 10)
                if frame[self.nbData - 1] == self.crcCheck(frame[0:self.nbData]):
                    for j in range(1):
                        # print("Acc:",(frame[1+(j*2)]<<8) + frame[2+(j*2)])
                        accX = ((frame[1+(j*2)]<<8) + frame[2+(j*2)])
                        accX = (accX - 0x10000)  if (accX > 0x7FFF) else accX

                        accY = ((frame[3+(j*2)]<<8) + frame[4+(j*2)])
                        accY = (accY - 0x10000)  if (accY > 0x7FFF) else accY         

                        accZ = ((frame[5+(j*2)]<<8) + frame[6+(j*2)]) 
                        accZ = (accZ - 0x10000)  if (accZ > 0x7FFF) else accZ     

                        self.all_accX.append(accX / self.accSensScaleFactor["2g"])
                        self.all_accY.append(accZ / self.accSensScaleFactor["2g"])
                        self.all_accZ.append(accZ / self.accSensScaleFactor["2g"])
                # print("Acc:",self.all_accX[-1])
                self.GraphAccX.setData(self.all_accX[-1000:])
                self.GraphAccY.setData(self.all_accY[-1000:])
                self.GraphAccZ.setData(self.all_accZ[-1000:])

    def crcCheck(self, frame):  
        crcValue = 0x00
        # original frame : b'U\xf9\xe4\xf9\xa4\xf0'
        # frame= b'U\xf9\xe4\xf9\xa4\xf0'
        for i in range(0,len(frame) - 1):
            # print("frame[",i,"]:",hex(frame[i]))
            crcValue = crcValue ^ frame[i]
        return crcValue

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    volume = IMUVisualizer()
    volume.show()
    app.exec_()