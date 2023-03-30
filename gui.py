import glob
import os.path

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import (QApplication, QDialog, QGraphicsView, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QSizePolicy,
                               QWidget, QMainWindow, QGraphicsScene)
import sys
import numpy as np
import time
from savorsense_ui import Ui_SavorSense
from nir import nir_sensor
from mmwave import mmwave
import threadin_fps
import cv2


configFileName = 'xwr68xxconfig.cfg'

directory = '/home/pi/raw_image'

CLIport = {}
Dataport = {}



class sense_gui(QMainWindow, Ui_SavorSense):
    def __init__(self):
        super(sense_gui, self).__init__()
        self.setupUi(self)

        self.start.clicked.connect(self.sensor_start)

    def sensor_start(self):
        self.nir_v.setText(str(self.get_nir()))
        self.mmwave_v.setText(str(self.get_mmwave()))
        image = self.capture_image()
        self.display_image(image)
        
        
        
    def display_image(self,image):
        img = image
        print(img)
        pixImg = QPixmap(img)
        scene = QGraphicsScene()
        scene.addPixmap(pixImg)
        self.graphicsView.setScene(scene)
        self.graphicsView.fitInView(scene.sceneRect())


    def capture_image(self):
        vs = threadin_fps.WebcamVideoStream(src=0).start()
        fps = threadin_fps.FPS().start()

        while fps._numFrames <= 5:
            frame = vs.read()
            name_image = threadin_fps.image_name()
            main_img_store_dir = os.path.join(directory, name_image)
            cv2.imwrite(main_img_store_dir, frame)
            fps.update()
        fps.stop()
        vs.stop()
        
        return main_img_store_dir


    def get_mmwave(self):
        CLIport, Dataport = mmwave.serialConfig(configFileName)
        configParameters = mmwave.parseConfigFile(configFileName)
        while True:
            try:
                dataOk, frameNumber, detObj = mmwave.readAndParseData14xx(Dataport, configParameters)
                if dataOk:
                    print(detObj)
                    mmwave_val = float(detObj['doppler'][1:2])
                    break
                time.sleep(0.033)  # Sampling frequency of 30 Hz (0.033)
            except KeyboardInterrupt:
                CLIport.write(('sensorStop\n').encode())
                CLIport.close()
                Dataport.close()

        return mmwave_val

    def get_nir(self):
        nir = nir_sensor()
        nir_value = nir.get_value()
        return nir_value



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = sense_gui()
    window.showMaximized()
    sys.exit(app.exec_())
