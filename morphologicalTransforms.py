import sys
import cv2
import numpy as np


## ------------ ALL MORPHOLOGICAL FILTERS ------------- ##

# Morph Helper Function is in main due to shared resources with the class!

def dilate(self):
    self.morphTransformHelper('dilate')

    kernel = np.ones((self.slider.value(), self.slider.value()), np.uint8)
    self.processedImage = cv2.dilate(self.processedImage, kernel, iterations=1)
    self.displayImage(2)


def erode(self):
    self.morphTransformHelper('erode')

    kernel = np.ones((5, 5), np.uint8)
    self.processedImage = cv2.erode(self.processedImage, kernel, iterations=1)
    self.displayImage(2)


def opening(self):
    self.morphTransformHelper('opening')

    kernel = np.ones((self.slider.value(), self.slider.value()), np.uint8)
    self.processedImage = cv2.morphologyEx(self.processedImage, cv2.MORPH_OPEN, kernel)
    self.displayImage(2)


def closing(self):
    self.morphTransformHelper('closing')

    self.processedImage = self.originalImage.copy()
    kernel = np.ones((self.slider.value(), self.slider.value()), np.uint8)
    self.processedImage = cv2.morphologyEx(self.processedImage, cv2.MORPH_CLOSE, kernel)
    self.displayImage(2)


def morphGradient(self):
    self.morphTransformHelper('morphGradient')

    kernel = np.ones((self.slider.value(), self.slider.value()), np.uint8)
    self.processedImage = cv2.morphologyEx(self.processedImage, cv2.MORPH_GRADIENT, kernel)
    self.displayImage(2)


def topHat(self):
    self.morphTransformHelper('topHat')

    kernel = np.ones((self.slider.value(), self.slider.value()), np.uint8)
    self.processedImage = cv2.morphologyEx(self.processedImage, cv2.MORPH_TOPHAT, kernel)
    self.displayImage(2)


def blackHat(self):
    self.morphTransformHelper('blackHat')

    kernel = np.ones((self.slider.value(), self.slider.value()), np.uint8)
    self.processedImage = cv2.morphologyEx(self.processedImage, cv2.MORPH_BLACKHAT, kernel)
    self.displayImage(2)


functions = (dilate , erode , opening , closing , morphGradient , topHat , blackHat )
