import glob
import os.path

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QBasicTimer)
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import (QApplication, QDialog, QGraphicsView, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QSizePolicy,
                               QWidget, QMainWindow, QGraphicsScene, QVBoxLayout, QProgressBar)
import sys
import numpy as np
import time
from savorsense_ui import Ui_SavorSense
from nir import nir_sensor
from mmwave import mmwave
import threadin_fps
import cv2
import datetime
import csv
import qwiic

import subprocess
sys.path.append("C:\git\pymmw-master\pymmw-master\source")

from pymmw import main_script


bus = '001'
device = '005'

path = '/dev/bus/usb/{0}/{1}'.format(bus, device)

configFileName = 'xwr68xxconfig.cfg'

directory = '/home/savormetrics/raw_image'

CLIport = {}
Dataport = {}


class sense_gui(QMainWindow, Ui_SavorSense):
    def __init__(self):
        super(sense_gui, self).__init__()
        self.setupUi(self)
        self.tray = 0
        self.start.clicked.connect(self.sensor_start)

    def sensor_start(self):
        print('BUTTON PUSHED')
        # t_end = time.time() + 60 * 7
        # self.tray = self.tray + 1
        # while time.time() <= t_end:
        curr = datetime.datetime.now()
        nir_1, nir_2 = self.get_nir()
        # mmwave = self.get_mmwave()
        mmwave = main_script(control_port="/dev/ttyUSB0", data_port="/dev/ttyUSB1")
        file_name = 'mois_1.csv'

            # self.show_countdown_dialog()
            # self.nir_v.setText(str(nir))
            # image = self.capture_image()
            # self.display_image(image)
            # self.mmwave_v.setText(str(mmwave))
        # self.write_to_csv(file_name, curr, self.tray, nir_1, nir_2, mmwave)
        # if time.time() >= t_end:
        #     print("-----------------end-------------------")
        #     break

    def display_image(self, image):
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
        frame = vs.read()
        name_image = threadin_fps.image_name()
        main_img_store_dir = os.path.join(directory, name_image)
        cv2.imwrite(main_img_store_dir, frame)
        fps.update()
        fps.stop()
        vs.stop()

        return main_img_store_dir

    def get_mmwave(self):
        count = 0
        CLIport, Dataport = mmwave.serialConfig(configFileName)
        configParameters = mmwave.parseConfigFile(configFileName)
        while True:
            try:
                dataOk, frameNumber, detObj = mmwave.readAndParseData14xx(Dataport, configParameters)
                if dataOk:
                    print(detObj)
                    mmwave_val = detObj
                    count = 0
                    break
                else:
                    count += 1
                    print(f'failed {count}')
                    if count == 5:
                        os.system("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind")
                        time.sleep(0.1)
                        os.system("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind")
                        time.sleep(1)
                        # self.get_mmwave()
                        CLIport, Dataport = mmwave.serialConfig(configFileName)
                        configParameters = mmwave.parseConfigFile(configFileName)
                        count = 0
                    # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                    # CLIport.write(b'softreset\n')
                    # subprocess.call(['sudo', './usbreset', path])
                    # CLIport, Dataport = mmwave.serialConfig(configFileName)
                    # configParameters = mmwave.parseConfigFile(configFileName)
                    # print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
                time.sleep(1)  # Sampling frequency of 30 Hz (0.033)
            except KeyboardInterrupt:
                CLIport.write(('sensorStop\n').encode())
                CLIport.close()
                Dataport.close()

        return mmwave_val

    def get_nir(self):
        nir = nir_sensor()
        nir_1, nir_2 = nir.get_value()
        return nir_1, nir_2

    def show_countdown_dialog(self):
        # Create the countdown dialog
        countdown_dialog = CountDownDialog()

        # Show the countdown dialog
        if countdown_dialog.exec_() == QDialog.Accepted:
            print("Countdown finished")

    def write_to_csv(self, csv_file, currtime, number, nir_1, nir_2, mmwave_v):
        t = currtime
        nir_1, nir_2 = nir_1, nir_2
        mmwave_v = mmwave_v
        csv_file = csv_file
        if not os.path.exists(csv_file):
            with open(csv_file, 'w+', newline='') as f:
                fw = csv.writer(f)
                fw.writerow([
                    'Date',
                    'Time',
                    'number',
                    'nir_1',
                    'nir_2',
                    'Doppler',
                ])
                fw.writerow([
                    t.strftime('%Y-%m-%d'),
                    t.strftime('%H-%M-%S'),
                    number,
                    nir_1,
                    nir_2,
                    mmwave_v,
                ])
        else:
            with open(csv_file, 'a', newline='') as f:
                fw = csv.writer(f)
                fw.writerow([
                    t.strftime('%Y-%m-%d'),
                    t.strftime('%H-%M-%S'),
                    number,
                    nir_1,
                    nir_2,
                    mmwave_v,
                ])


class CountDownDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Warning!")
        self.resize(400, 300)
        self.setModal(True)

        self.label_1 = QLabel(self)
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.setText('The device is in calibration station, the falling number range will be -30% to 30%.')

        # Create the progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 60000)
        self.progress_bar.setValue(60000)

        # Create the label
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("1:00")

        # Add the progress bar and label to a vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_1)
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        # Start the countdown timer
        self.timer = QBasicTimer()
        self.timer.start(1000, self)

    def timerEvent(self, event):
        # Update the label and progress bar
        remaining_time = self.progress_bar.value() - 1000
        self.progress_bar.setValue(remaining_time)
        self.label.setText("{:d}:{:02d}".format(remaining_time // 60000, (remaining_time // 1000) % 60))
        # Close the dialog when the countdown is finished
        if remaining_time == 0:
            self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = sense_gui()
    window.showMaximized()
    sys.exit(app.exec_())
