import cv2
import numpy as np


def applyCornerDetectionHelper(self, currentAlgorithm):
    if currentAlgorithm == 'ShiThomsiCornerDetection':
        self.shiThomasiGoodFeaturesClicked()
    elif currentAlgorithm == 'harrisonCornerDetection':
        self.harrisCornerDetector()
    elif currentAlgorithm == 'FASTCornerDetection':
        self.harrisCornerDetector()


def applyCornerDetection(self):
    self.applyCornerDetectionHelperFunction()
    self.filterFlag = 3
    currentTool = self.cornerDetectionQComboBox.currentText()
    self.applyCornerDetectionHelper(currentTool)


def shiThomasiGoodFeaturesClicked(self):
    currFilter = "ShiThomsiCornerDetection"
    print('Applying Filter : ', currFilter)
    self.lastFilter = 'ShiThomsiCornerDetection'
    self.initializeSlider(s=0, e=50)
    self.processedImage = self.originalImage.copy()
    gray = self.processedImage
    img = self.processedImage
    if len(self.processedImage.shape) > 2:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(gray, self.slider.value(), 0.01,
                                      10)  # params are image, number of points, threshold(here it is
    # set to low) and 10(unknown)
    corners = np.int0(corners)

    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 3, (255, 255, 255), -1)

    self.processedImage = img.copy()
    self.displayImage(2)


def harrisCornerDetector(self):
    currFilter = "harrisonCornerDetection"
    print("Applying Filter : ", currFilter)
    self.processedImage = self.originalImage.copy()
    self.lastFilter = 'harrisonCornerDetection'
    self.initializeSlider(s=0, e=50)
    self.processedImage = self.originalImage.copy()
    gray = self.processedImage
    img = self.processedImage

    if len(self.processedImage.shape) > 2:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
    dst = cv2.dilate(dst, None)

    img[dst > (self.slider.value() / 500.0) * dst.max()] = [0, 0, 255]
    self.processedImage = img.copy()
    self.displayImage()


def fastCornerDetector(self):
    currFilter = 'FASTCornerDetection'
    print("Applying Filter : ", currFilter)
    self.processedImage = self.originalImage.copy()
    self.lastFilter = 'FASTCornerDetection'
    self.initializeSlider(s=0, e=50)
    self.processedImage = self.originalImage.copy()
    gray = self.processedImage
    img = self.processedImage

    if len(self.processedImage.shape) > 2:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Initiate FAST object with default values
    fast = cv2.FastFeatureDetector()

    # find and draw the keypoints
    kp = fast.detect(gray, None)
    img2 = cv2.drawKeypoints(img, kp, color=(255, 0, 0))

    # Print all default params
    print("Threshold: ", fast.getInt('threshold'))
    print("nonmaxSuppression: ", fast.getBool('nonmaxSuppression'))
    print("neighborhood: ", fast.getInt('type'))
    print("Total Keypoints with nonmaxSuppression: ", len(kp))
    self.processedImage = img2.copy()
    self.displayImage()


functions = (shiThomasiGoodFeaturesClicked, applyCornerDetectionHelper, applyCornerDetection, harrisCornerDetector,
             fastCornerDetector)
