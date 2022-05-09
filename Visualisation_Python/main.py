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
    nbData = 26 # number of data per frame

    # accelerometer sensitivity scale factor corresponding to {2g,4g,8g,16g}
    accSensScaleFactor = {"2g"  : 16384, 
                          "4g"  : 8192,
                          "8g"  : 4096,
                          "16g" : 2048}
    gyroSensScaleFactor = {"250dps" : 131, 
                          "500dps"  : 65.5,
                          "1000dps" : 32.8,
                          "2000dps" : 16.4}

    all_accX = []
    all_accY = []
    all_accZ = []

    all_gyroX = []
    all_gyroY = []
    all_gyroZ = []

    def __init__(self, steps=5, *args, **kwargs):
        super(IMUVisualizer, self).__init__(*args, **kwargs)
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.createWindow()
        try:
            self.serialPort = ps.Serial('COM3', 115200, timeout=0)
            self.serialPort.close()
            self.serialPort.open()
            if self.serialPort.isOpen():
                self.serialPort.flushInput()
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

        pg.setConfigOptions()
        self.view = pg.GraphicsLayoutWidget()


        # set visualise tab

        self.plotItemAccX = self.view.addPlot(title="AccX")
        self.plotItemAccY = self.view.addPlot(title="AccY")
        self.plotItemAccZ = self.view.addPlot(title="AccZ")
        self.view.nextRow()

        self.plotItemGyroX = self.view.addPlot(title="GyroX")
        self.plotItemGyroY = self.view.addPlot(title="GyroY")
        self.plotItemGyroZ = self.view.addPlot(title="GyroZ")
        self.view.nextRow()

        self.plotItemMagnX = self.view.addPlot(title="MagnX")
        self.plotItemMagnY = self.view.addPlot(title="MagnY")
        self.plotItemMagnZ = self.view.addPlot(title="MagnZ")

        # set limits 
        self.plotItemAccX.setYRange(-2,2)
        self.plotItemAccY.setYRange(-2,2)
        self.plotItemAccZ.setYRange(-2,2)

        self.plotItemGyroX.setYRange(-250,250)
        self.plotItemGyroY.setYRange(-250,250)
        self.plotItemGyroZ.setYRange(-250,250)


        self.GraphAccX = self.plotItemAccX.plot()
        self.GraphAccY = self.plotItemAccY.plot()
        self.GraphAccZ = self.plotItemAccZ.plot()



        self.GraphGyroX = self.plotItemGyroX.plot()
        self.GraphGyroY = self.plotItemGyroY.plot()
        self.GraphGyroZ = self.plotItemGyroZ.plot()

        self.GraphMagnX = self.plotItemMagnX.plot()
        self.GraphMagnY = self.plotItemMagnY.plot()
        self.GraphMagnZ = self.plotItemMagnZ.plot()

        # QPushButtons
        self.runVisualiser = QtWidgets.QPushButton("Run")
        self.stopVisualiser = QtWidgets.QPushButton("Stop")

        TmpLayout = QtWidgets.QVBoxLayout()
        TmpLayout.addWidget(self.view)
        TmpLayout.addWidget(self.runVisualiser)
        TmpLayout.addWidget(self.stopVisualiser)
        
        self.tabVisualise.setLayout(TmpLayout)


        



        
        # self.view.show()
    def readFrame(self):
        if (self.serialPort.inWaiting() >= self.nbData):
            frame = self.serialPort.read(self.nbData)
            if frame == b'': return
            elif frame[0] == 0x55:
                if len(frame) < self.nbData:
                    print("Frame:",frame.hex('-'),";len:",len(frame))
                    return
                # print("Frame:",frame.hex('-'),";len:",len(frame))
                # print("CrcFrame:",hex(frame[self.nbData - 1]))
                # print("subFrame:",frame[0:self.nbData - 1].hex('-'))
                # print("CrcSubFrame:",hex(self.crcCheck(frame[0:self.nbData])))
                # print('-' * 10)
                if frame[self.nbData - 1] == self.crcCheck(frame[0:self.nbData]):
                    for j in range(2):
                        # print("Acc:",(frame[1+(j*2)]<<8) + frame[2+(j*2)])
                        accX = ((frame[1+(j*2)]<<8) + frame[2+(j*2)])
                        # print("X:", accX)
                        accX = (accX - 0x10000)  if (accX > 0x7FFF) else accX
                        self.all_accX.append(accX / self.accSensScaleFactor["2g"])

                    for j in range(2):
                        accY = ((frame[5+(j*2)]<<8) + frame[6+(j*2)])
                        # print("Y:", accY)
                        accY = (accY - 0x10000)  if (accY > 0x7FFF) else accY   
                        self.all_accY.append(accY / self.accSensScaleFactor["2g"])

                    for j in range(2):
                        accZ = ((frame[9+(j*2)]<<8) + frame[10+(j*2)]) 
                        # print("Z:", accZ)
                        accZ = (accZ - 0x10000)  if (accZ > 0x7FFF) else accZ     
                        self.all_accZ.append(accZ / self.accSensScaleFactor["2g"])


                    # Gyroscope   
                    for j in range(2):
                        # print("Acc:",(frame[1+(j*2)]<<8) + frame[2+(j*2)])
                        gyroX = ((frame[13+(j*2)]<<8) + frame[14+(j*2)])
                        # print("X:", accX)
                        gyroX = (gyroX - 0x10000)  if (gyroX > 0x7FFF) else gyroX
                        self.all_gyroX.append(gyroX / self.gyroSensScaleFactor["250dps"])

                    for j in range(2):
                        gyroY = ((frame[17+(j*2)]<<8) + frame[18+(j*2)])
                        # print("Y:", accY)
                        gyroY = (gyroY - 0x10000)  if (gyroY > 0x7FFF) else gyroY   
                        self.all_gyroY.append(gyroY / self.gyroSensScaleFactor["250dps"])

                    for j in range(2):
                        gyroZ = ((frame[21+(j*2)]<<8) + frame[22+(j*2)]) 
                        # print("Z:", accZ)
                        gyroZ = (gyroZ - 0x10000)  if (gyroZ > 0x7FFF) else gyroZ     
                        self.all_gyroZ.append(gyroZ / self.gyroSensScaleFactor["250dps"])

                else :
                    print("CRC error!")       
                        
                        
                # print("AccX:",self.all_accX[-1])
                # print("AccY:",self.all_accY[-1])
                # print("AccZ:",self.all_accZ[-1])
                self.GraphAccX.setData(self.all_accX[-1000:])
                self.GraphAccY.setData(self.all_accY[-1000:])
                self.GraphAccZ.setData(self.all_accZ[-1000:])
                self.GraphGyroX.setData(self.all_gyroX[-1000:])
                self.GraphGyroY.setData(self.all_gyroY[-1000:])
                self.GraphGyroZ.setData(self.all_gyroZ[-1000:])
        else:
            print('not enough data')

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