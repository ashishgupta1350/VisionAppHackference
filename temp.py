# latest Image Processing applied
# helps apply image processing tools to images.

import cv2
import numpy as np


class filter():
    def __init__(self):
        super().__init__()
        # self.initFilters()
        self.currentThreshold_Input = ''
        self.processedImage = None

    def initFilters(self):
        self.currentThreshold_Input = str(input('Please enter the filter'))
        threshold(self.currentThreshold_Input)

    def setImage(self, myImage):
        self.processedImage = cv2.imread(myImage)

    def threshold(self, currentThreshold):

        if len(self.processedImage.shape) > 2:
            self.processedImage = cv2.cvtColor(self.processedImage, cv2.COLOR_BGR2GRAY)
        # self.displayImage()

        # cant use a switch case because the names are strings and not int. I can convert them to int by having case(
        # 1) : threshold='BinaryThreshold' break but it is too long
        if currentThreshold == 'BinaryThreshold':

            ret, self.processedImage = cv2.threshold(self.processedImage, 20, 255, cv2.THRESH_BINARY)
        elif currentThreshold == 'BinaryInverseThreshold':

            ret, self.processedImage = cv2.threshold(self.processedImage, 20, 255,
                                                     cv2.THRESH_BINARY_INV)
        elif currentThreshold == 'TruncThreshold':

            ret, self.processedImage = cv2.threshold(self.processedImage, 20, 255, cv2.THRESH_TRUNC)
        elif currentThreshold == 'TozeroThreshold':

            ret, self.processedImage = cv2.threshold(self.processedImage, 20, 255, cv2.THRESH_TOZERO)
        elif currentThreshold == 'TozeroThresholdInverse':

            ret, self.processedImage = cv2.threshold(self.processedImage, 20, 255,
                                                     cv2.THRESH_TOZERO_INV)
        elif currentThreshold == 'AdaptiveThreshold_Mean_C':

            self.processedImage = cv2.adaptiveThreshold(self.processedImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                        cv2.THRESH_BINARY, self.slider.value(), 2)
        elif currentThreshold == 'AdaptiveThreshold_Gaussian':

            self.processedImage = cv2.adaptiveThreshold(self.processedImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                        cv2.THRESH_BINARY, self.slider.value(), 2)
        elif currentThreshold == 'OtsuThreshold':

            ret2, self.processedImage = cv2.threshold(self.processedImage, self.slider.value(), 255, cv2.THRESH_BINARY,
                                                      cv2.THRESH_OTSU)

        self.displayImage()

    def displayImage(self):
        while (True):
            cv2.imshow('Image', self.processedImage)
            k = cv2.waitKey(1) & 0xFF

            if k == 0 or k == ord('q'):
                break
        cv2.destroyAllWindows()


myFilter = filter()

myFilter.setImage('image.jpg')  # choose the image here

myFilter.threshold('BinaryInverseThreshold')

myFilter.displayImage()
