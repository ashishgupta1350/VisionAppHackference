# latest Image Processing applied
# helps apply image processing tools to images.

import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore

import InteractiveGrabcut  # not working right now!


def applyImageProcessingHelper(self, currentTool):
    self.processedImage = self.originalImage.copy()
    self.imageProcessingCodeHelper() # gets the code to the getCode() button method
    if currentTool == 'DetectContours':
        print()
        print()
        print('Detect Contours called')
        print(
            'Contours are detected on a thresholded image, that is 2 channel. So it is better to threshold the '
            'image before applying this filter! MinVal for slider is 20(Lower limit of threshold)')
        print(
            'Alternately, if not done, then select the value of the slider and then apply filter to threshold '
            'automatically. It is recommended to set slider at 127 for this filter!')
        self.lastFilter = 'DetectContours'

        self.initializeSlider(s=20, e=255)
        processed = self.originalImage.copy()
        # change the self.processedImage

        if len(self.processedImage.shape) >= 3:
            imGray = cv2.cvtColor(self.processedImage, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imGray, self.slider.value(), 255, 0)
            processed = thresh.copy()
        else:
            print()
            print()
            print('Print Current Contours called')
            print(
                'Not applying automatic internal threshold on image, since image is already grayscaled. It is '
                'assumed that you applied a suitable filter!')
        _, contours, _ = cv2.findContours(processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(self.processedImage, contours, -1, (255, 0, 0), 4)
        # highlight the individual contours with different color
        for cnt in range(len(contours)):
            cv2.drawContours(self.processedImage, [contours[cnt]], -1,
                             self.colorContainer[cnt % len(self.colorContainer)], 2)


    elif currentTool == 'PrintCurrentContours':
        self.lastFilter = 'PrintCurrentContours'
        self.initializeSlider(s=20, e=255)
        processed = self.originalImage.copy()
        if len(self.processedImage.shape) >= 3:
            print('Taking contours from updated original image. Please click update original before applying this!')
            imGray = cv2.cvtColor(self.originalImage, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imGray, self.slider.value(), 255, 0)
            processed = thresh.copy()
        else:
            print(
                'Not applying automatic internal threshold on image, since image is already grayscaled. It is '
                'assumed that you applied a suitable filter!')
        _, contours, _ = cv2.findContours(processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print('Contours are :')
        for cnt in range(len(contours)):
            print(cnt, ' : ', contours[cnt])

    elif currentTool == 'GetHistogram':
        try:
            import matplotlib.pyplot as plt
        except:
            print('Install Matplotlib first')
            return
        print()
        print()
        print('Get Histogram Called')
        self.lastFilter = 'GetHistogram'
        self.initializeSlider(s=20, e=255)
        processed = self.originalImage.copy()
        if len(self.processedImage.shape) >= 3:
            processed = cv2.cvtColor(self.originalImage, cv2.COLOR_BGR2GRAY)

        img = processed
        plt.hist(img.ravel(), 256, [0, 256])
        plt.title('Histogram')
        plt.show()

    elif currentTool == 'Get2DHistogram':
        try:
            import matplotlib.pyplot as plt
        except:
            print('Install Matplotlib first')
            return
        print()
        print()
        print('Get 2D Histogram Called on colored image')
        self.lastFilter = 'Get2DHistogram'
        self.initializeSlider(s=20, e=255)  # it sets the slider and updates the text label
        # processed = None
        img = self.originalImage.copy()
        if len(img.shape) == 2:
            print('Image is grayscale! Applying GetHistograms')
            self.applyImageProcessingHelper('GetHistogram')
            return
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

        plt.imshow(hist, interpolation='nearest')
        plt.title('Colored2DHistogram')
        plt.show()

    elif currentTool == 'HoughLineTransform':

        print()
        print()
        print('Hough Line Transform Called')
        self.lastFilter = 'HoughLineTransform'
        self.initializeSlider(s=20, e=255)  # it sets the slider and updates the text label
        img = self.originalImage.copy()
        gray = img.copy()
        if len(img) >= 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        if len(lines) > 0:
            for rho, theta in lines[0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 4)

        self.processedImage = img.copy()

    elif currentTool == 'InteractiveGrabcut':
        print()
        print()
        print('Interactive Grabcut Called')
        self.lastFilter = 'InteractiveGrabcut'
        print('Works as follows: ')
        print('Click and drag across a object that you want to extract!')
        print('The object will be grabbed and mask will show the grab.')
        print('It might happen that algo leaves some areas. Then those areas can be added by refine selection!')
        self.initializeSlider(s=20, e=255)  # it sets the slider and updates the text label
        self.processedImage = InteractiveGrabcut.initializeGrabCut(self.processedImage)

    elif currentTool == 'HuffCircleTransform':
        print()
        print()
        print('HuffCircleTransform Called')
        self.lastFilter = 'HuffCircleTransform'

        self.initializeSlider(s=20, e=255)  # it sets the slider and updates the text label

        img = self.processedImage
        if (len(img.shape) > 2):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.medianBlur(img, 5)
            cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    self.displayImage(2)


# @pyqtSlot()
def applyImageProcessing(self):
    self.filterFlag = 2  # to let the slider know we are using the image processing tools
    currentTool = self.imageProcessingQComboBox.currentText()
    self.applyImageProcessingHelper(currentTool)


# Image Processing ends
# @pyqtSlot()
def applyThresholds(self):
    self.filterFlag = int(1)
    currentThreshold = self.thresholds.currentText()
    self.threshold(currentThreshold)


# @pyqtSlot()
def applyFilter(self):
    currFilter = self.filters.currentText()
    self.filterFlag = int(0)
    print('Applying Filter : ', currFilter)
    self.filterApply(currFilter)


def swapColor(self):
    self.displayImage(2, True)


def checkProcessedImage(self):
    if self.processedImage == None:
        self.processedImage = self.image.copy()
        print('Please Reload the image!')
    return


def filterApply(self, currFilter):
    self.imageProcessingCodeHelper()
    self.processedImage = self.originalImage.copy()

    # self.checkProcessedImage()
    if currFilter == 'Canny':
        print('Applying Canny')
        self.lastFilter = 'Canny'
        self.initializeSlider(s=0, e=300)
        gray = self.processedImage
        if len(self.processedImage.shape) > 2:
            gray = cv2.cvtColor(self.processedImage,
                                cv2.COLOR_BGR2GRAY)  # if len(self.image.shape) >= 3 else self.originalImage
        self.processedImage = cv2.Canny(gray, self.slider.value(), self.slider.value() * 3)

    elif currFilter == 'ColorSwap':
        self.lastFilter = 'ColorSwap'
        self.initializeSlider()
        qformat = QImage.Format_Indexed8

        if len(self.processedImage.shape) == 3:  # rows cols and color channel.

            if self.processedImage.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(self.originalImage, self.originalImage.shape[1], self.originalImage.shape[0],
                     self.originalImage.strides[0], qformat)
        # img = img.rgbSwapped()  # -->  This is not to be done here
        self.imageLabel.setPixmap(QPixmap.fromImage(img))
        self.imageLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        return

    elif currFilter == 'Moziac':
        self.lastFilter = 'Moziac'
        self.initializeSlider()
        qformat = QImage.Format_Indexed8

        if len(self.processedImage.shape) == 3:  # rows cols and color channel.
            if self.processedImage.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(self.processedImage, self.processedImage.shape[1], self.processedImage.shape[0],
                     self.processedImage.strides[0], qformat)
        # img=img.rgbSwapped()  #-->  This is not to be done here
        self.imageLabel.setPixmap(QPixmap.fromImage(img))
        self.imageLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        return

    elif currFilter == 'Grayscale':
        self.lastFilter = 'GrayScale'
        self.initializeSlider()

        self.processedImage = self.originalImage
        if len(self.processedImage.shape) > 2:
            self.processedImage = cv2.cvtColor(self.processedImage, cv2.COLOR_BGR2GRAY)

    elif currFilter == 'GaussianBlur':
        self.lastFilter = 'GaussianBlur'
        self.initializeSlider(s=1, e=21)
        if self.slider.value() % 2 == 0: self.slider.setValue(self.slider.value() + 1)
        self.processedImage = cv2.GaussianBlur(self.processedImage, (self.slider.value(), self.slider.value()), 0)

    elif currFilter == 'MedianFilter':
        self.lastFilter = 'MedianFilter'
        self.initializeSlider(s=1, e=21)
        if self.slider.value() % 2 == 0: self.slider.setValue(self.slider.value() + 1)
        self.processedImage = cv2.medianBlur(self.processedImage, self.slider.value())

    elif currFilter == 'BilateralFilter':
        self.lastFilter = 'BilateralFilter'
        self.initializeSlider(s=1, e=20)
        self.processedImage = cv2.bilateralFilter(self.processedImage, self.slider.value(), 75, 75)

    elif currFilter == 'Geometric 1':
        self.lastFilter = 'Geometric 1'
        self.initializeSlider()
        rows = self.processedImage.shape[1]
        cols = self.processedImage.shape[2]
        # we can have 2 sliders here and then we can take input from those sliders. how to decativate the sliders
        # is what we have to see
        M = np.float32([[1, 0, 200], [0, 1, 250]])

        self.processedImage = cv2.warpAffine(self.processedImage, M, (cols, rows))
    elif currFilter:
        # if current filter is not none
        self.threshold(self.lastFilter)
    self.displayImage(2)


def threshold(self, currentThreshold):
    self.lastFilter = currentThreshold
    self.thesholdCodeHelper()
    self.processedImage = self.originalImage.copy()
    if self.grayCheck.isChecked:
        if len(self.processedImage.shape) > 2:
            self.processedImage = cv2.cvtColor(self.processedImage, cv2.COLOR_BGR2GRAY)
        self.displayImage(2)
    else:
        self.processedImage = self.originalImage.copy()
        self.displayImage(2)
    # cant use a switch case because the names are strings and not int. I can convert them to int by having case(
    # 1) : threshold='BinaryThreshold' break but it is too long
    if currentThreshold == 'BinaryThreshold':
        self.lastFilter = 'BinaryThreshold'
        self.initializeSlider(s=0, e=255)
        ret, self.processedImage = cv2.threshold(self.processedImage, self.slider.value(), 255, cv2.THRESH_BINARY)
    elif currentThreshold == 'BinaryInverseThreshold':
        self.lastFilter = 'BinaryInverseThreshold'
        self.initializeSlider(s=0, e=255)
        ret, self.processedImage = cv2.threshold(self.processedImage, self.slider.value(), 255,
                                                 cv2.THRESH_BINARY_INV)
    elif currentThreshold == 'TruncThreshold':
        self.lastFilter = 'TruncThreshold'
        self.initializeSlider(s=0, e=255)
        ret, self.processedImage = cv2.threshold(self.processedImage, self.slider.value(), 255, cv2.THRESH_TRUNC)
    elif currentThreshold == 'TozeroThreshold':
        self.lastFilter = 'TozeroThreshold'
        self.initializeSlider(s=0, e=255)
        ret, self.processedImage = cv2.threshold(self.processedImage, self.slider.value(), 255, cv2.THRESH_TOZERO)
    elif currentThreshold == 'TozeroThresholdInverse':
        self.lastFilter = 'TozeroThresholdInverse'
        self.initializeSlider(s=0, e=255)
        ret, self.processedImage = cv2.threshold(self.processedImage, self.slider.value(), 255,
                                                 cv2.THRESH_TOZERO_INV)
    elif currentThreshold == 'AdaptiveThreshold_Mean_C':
        self.lastFilter = 'AdaptiveThreshold_Mean_C'
        self.initializeSlider(s=3, e=21)
        if self.slider.value() % 2 == 0: self.slider.setValue(self.slider.value() + 1)
        self.processedImage = cv2.adaptiveThreshold(self.processedImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                    cv2.THRESH_BINARY, self.slider.value(), 2)
    elif currentThreshold == 'AdaptiveThreshold_Gaussian':
        self.lastFilter = 'AdaptiveThreshold_Gaussian'
        self.initializeSlider(s=3, e=15)
        if self.slider.value() % 2 == 0: self.slider.setValue(self.slider.value() + 1)
        self.processedImage = cv2.adaptiveThreshold(self.processedImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                    cv2.THRESH_BINARY, self.slider.value(), 2)
    elif currentThreshold == 'OtsuThreshold':
        self.lastFilter = 'OtsuThreshold'
        self.initializeSlider(s=0, e=255)
        ret2, self.processedImage = cv2.threshold(self.processedImage, self.slider.value(), 255, cv2.THRESH_BINARY,
                                                  cv2.THRESH_OTSU)

    self.displayImage(2)


functions = (
    applyImageProcessingHelper, applyImageProcessing, applyImageProcessing, applyThresholds, applyFilter, swapColor,
    checkProcessedImage,
    filterApply,
    threshold
)
