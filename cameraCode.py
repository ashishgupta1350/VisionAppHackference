

## ------------- Camera Code ------------- ##
import cv2
from PyQt5.QtCore import QTimer


def camButtonStartClicked(self):
    self.cameraCodeHelper()
    self.lastFilter = 'Camera Active'
    self.initializeSlider()
    self.cap = cv2.VideoCapture(0)
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.updateFrame)
    self.timer.start(5)


def updateFrame(self):
    ret, self.processedImage = self.cap.read()

    if ret:
        self.processedImage = cv2.flip(self.processedImage, 1)
        if self.detectFaceCheckbox.isChecked():
            if self.detectEye.isChecked():
                self.actionFaceDetectionClicked(1)
            else:
                self.actionFaceDetectionClicked(0)

            return
        self.displayImage(2)
    else:
        self.processedImage = cv2.flip(self.processedImage, 1)
        self.displayImage(2)
        print('Failed to read from camera, Program will exit.')
        self.camButtonStopClicked()


def camButtonStopClicked(self):
    self.cap.release()
    self.timer.stop()
    self.lastFilter = 'Camera Passive'
    self.initializeSlider()


## ************* Camera Code End ************ ##

functions = (camButtonStartClicked, camButtonStopClicked, updateFrame)