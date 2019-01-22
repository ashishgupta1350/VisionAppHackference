import sys
import webbrowser

try:
    import urllib.request
    import numpy as np
except:
    print('Install urllib and numpy to use mobile cam else it will now work')

try:
    import cv2
except:
    print('Please install OpenCV first to run this!')
    exit(1)

try:
    from PyQt5 import QtCore
    from PyQt5 import uic
    from PyQt5.QtCore import pyqtSlot, QTimer
    from PyQt5.QtGui import QImage, QPixmap, QIcon
    from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox, QAction, QMainWindow, QLineEdit, QPushButton, \
    QInputDialog, QWidget, QFormLayout, QTextBrowser
except:
    print("Please install PyQt5 first to run the interface!")
    exit(1                              )

try:
    import matplotlib.pyplot as plt
except:
    print('Please install matplotlib, some features like [Histograms] will not work')

# Py files for additional features
import ChromeDinasourGamePakhi

# I have a filter flag, for slider. Now as soon as I apply a certain filter, the lastFilter and FilterFlag will be set.
# Now when I change the slider, I would know, which function to activate and change values to.


# -- Decorators -- #
# This code uses decorators to import class functions. To add any function filled file, just add ( +
# file_name.functions) in it. for that, we need 1) import the file 2) In file, add functions as a variable and
# functions = ( function_names, .., .., ..), 3) add to below lib function! End:)

import lib
import morphologicalTransforms
import encryptionCode
import paintCode
import ImageProcessingFilters
import cameraCode
import cornerDetection
import videoEncryption

# Global Variables for multi window code
IPCamURL = ''
IPCamFlag = False
codeString = '<b> No code selected yet </b>' \
             '\n'


class textEditor(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        uic.loadUi(r'assets/textEditor.ui', self)
        self.initializeButtons()
        self.setWindowTitle('<Code>')
        self.show()
        self.textBrowser.setText(codeString)
        self.textBrowser.setAcceptRichText(True)
        qtb = QTextBrowser()
        qtb.setAcceptRichText(True)
        qtb.setText(codeString)


    def initializeButtons(self):
        self.okButton.clicked.connect(self.okButtonClicked)
        self.openCode.clicked.connect(self.openCodeClicked)

    def okButtonClicked(self):
        self.close()
    def openCodeClicked(self):

        # self.lastFilter = 'Video Encryption'
        # self.initializeSlider()
        self.codeString = ''
        file = open(r'assets/codeSamples/thresholdCode.txt')
        for line in file:
            self.codeString = self.codeString + line
        global codeString
        codeString = self.codeString
        file.close()
        file = open('assets/codeSamples/code.txt')
        file.write(codeString)
        file.close()

class IPCamDialog(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.label1 = QLineEdit('http://192.168.12.160:8080', self)
        self.label1.move(10, 50)
        self.label1.setFixedWidth(230)
        # btn1 = QPushButton("Button 1", self)
        # btn1.move(30, 50)

        self.btn2 = QPushButton("OK", self)
        self.btn2.move(250, 50)

        self.btn2.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(300, 300, 360, 100)
        self.setWindowTitle('Set IP for IPCAM')
        self.show()

    def buttonClicked(self):
        global IPCamURL
        IPCamURL = str(self.label1.text()) # get the url from the source!
        print('Debug -- in class')
        IPCamURL = IPCamURL + '/shot.jpg'
        IPCamFlag = True
        print(IPCamURL)
        cv2.destroyAllWindows()
        self.close()



@lib.add_functions_as_methods(
    morphologicalTransforms.functions
    + encryptionCode.functions
    + paintCode.functions
    + ImageProcessingFilters.functions
    + cameraCode.functions
    + cornerDetection.functions
    + videoEncryption.functions
)

class gui(QMainWindow):
    # init class
    def __init__(self):
        super(gui, self).__init__()
        print(
            'Welcome to Mini Photoshop. This Gui is designed to edit photos. You can apply filters, detect faces and '
            'eyes in image, encrypt the data in the image and a lot more!\n\n\n')
        uic.loadUi(r'assets/miniPhotoshopDesignMainWindow_Paint.ui', self)

        self.initializePaint()
        self.cap = None
        self.globalDrawing = False
        self.processedImage = cv2.imread(r'images/img22.jpg')
        self.originalImage = cv2.imread(r'images/img22.jpg')
        self.displayImage(2)
        self.filterFlag = int(1)
        self.lastFilter = 'No Filter Used'
        self.initializeSlider()
        self.colorContainer = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0),
                               (255, 255, 255), (100, 100, 100), (100, 100, 255), (100, 255, 100), (255, 100, 0),
                               (0, 100, 200)]
        self.codeString = codeString
        self.mainCodeHelper() # To load main code .py to getCode() button




        # Video Encryption
        self.videoData = None
        self.videoName = None
        self.imageFolder = '/EncryptedImages'
        self.myImage = QPixmap("stenographyImage.jpg")
        self.imageLabel.setPixmap(self.myImage)
        self.videoName = 'input.mp4'

        try:
            self.videoName = 'input.mp4'
        except:
            self.videoName = None
        self.encryptButton.clicked.connect(self.readDataToVideo)
        self.decryptButton.clicked.connect(self.decryptDataFromVideo)
        # Video Encryption Code Ends




        #IP Cam code
        self.ipCamURL = 'http://192.168.1.5:8080/shot.jpg'
        self.nd = 0  # this is for example GUI on button clicked
        self.ipCamIpButton.clicked.connect(self.loadVideoFromMobile)
        self.mobileCamButton.clicked.connect(self.loadVideoFromMobileHelper)


        # Load Save and Reset Buttons
        self.loadButton.clicked.connect(self.loadClicked)
        self.saveButton.clicked.connect(self.saveClicked)
        self.resetButton.clicked.connect(self.resetClicked)

        # Filter, Thresholds, Image Processing QCombo Boxes
        self.filters.activated.connect(self.applyFilter)
        self.thresholds.activated.connect(self.applyThresholds)
        self.imageProcessingQComboBox.activated.connect(self.applyImageProcessing)

        # Face Filters
        self.faceQComboBox.activated.connect(self.applyFacialFilters)

        # update original image (V important)
        self.updateOriginal.clicked.connect(self.updateOriginalImage)

        # About and instructions buttons
        self.aboutButton.clicked.connect(self.aboutClicked)
        self.instructionButton.clicked.connect(self.instructionClicked)

        self.slider.valueChanged.connect(self.sliderClicked)
        self.lineEditSliderValue.returnPressed.connect(self.lineEditSliderValueClicked)
        self.mainMenuClicked()

        # Camera Buttons
        self.camButtonStart.clicked.connect(self.camButtonStartClicked)
        self.camButtonStop.clicked.connect(self.camButtonStopClicked)

        # Paint Buttons
        # self.paintButtonStart.clicked.connect(self.paintButtonStartClicked)
        # self.paintButtonStop.clicked.connect(self.paintButtonStopClicked)

        # Face Detection:
        self.face_cascade = cv2.CascadeClassifier(
            r'assets/haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(
            r'assets/haarcascade_eye.xml')
        # self.actionFaceDetection.triggered.connect(self.actionFaceDetectionClicked)

        # image encryption and watermark
        self.watermarkImage.clicked.connect(self.waterMarkImageClicked)
        self.encryptData.clicked.connect(self.encryptDataClicked)
        self.decryptData.clicked.connect(self.decryptDataClicked)
        self.checkWatermarkButton.clicked.connect(self.checkWatermark)

        # play button
        self.playButton.clicked.connect(self.playButtonClicked)

        # Video Load button
        self.loadVideoButton.clicked.connect(self.loadVideoButtonClicked)
        self.stopVideoButton.clicked.connect(self.stopVideoButtonClicked)
        self.stopVideo = False

        # corner Detection buttons
        self.cornerDetectionQComboBox.activated.connect(self.applyCornerDetection)

        # mobile cam

        # rotation code
        # self.rotateLeftButton.clicked.connect(self.rotateButtonLeftClicked)
        # self.rotateRightButton.clicked.connect(self.rotateButtonRightClicked)

        # menu and menu within menu
        self.createMenuBar()

        # getCode
        self.getCodeButton.clicked.connect(self.getCodeButtonClicked)

        # Paint2.0 initialization
        # global vars for paint

        self.backupImage = None
        self.img = None
        self.prevX = None
        self.prevY = None
        self.localMouseDown = False

        self.paint2Button.clicked.connect(self.paintButtonClicked)


        # code.py functionality
        # self.openCode.clicked.connect(self.openCodeInPython)

    def getCodeButtonClicked(self):
        codeEditor = textEditor(self)
        codeEditor.show()


    #Helper functions for getting code in getCode button!

    def morphTransformHelper(self, transform):

        self.filterFlag = 0
        print('Running ',transform)
        self.lastFilter = transform
        self.initializeSlider()
        self.processedImage = self.originalImage.copy()

        self.codeString = ''
        file = open(r'assets/codeSamples/morphTransforms.txt')
        for line in file:
            self.codeString = self.codeString + line
        global codeString
        codeString = self.codeString
        file.close()

    def cameraCodeHelper(self):
        self.codeString = ''
        file = open(r'assets/codeSamples/cameraCode.txt')
        for line in file:
            self.codeString = self.codeString + line
        global codeString
        codeString = self.codeString
        file.close()

    def applyCornerDetectionHelperFunction(self): #function added because helper<< is already a function
        self.codeString = ''
        file = open(r'assets/codeSamples/cornerDetection.txt')
        for line in file:
            self.codeString = self.codeString + line
        global codeString
        codeString = self.codeString
        file.close()
    def paintCodeHelper(self):
        self.codeString = ''
        file = open(r'assets/codeSamples/paintCode.txt')
        for line in file:
            self.codeString = self.codeString + line
        global codeString
        codeString = self.codeString
        file.close()

    def playButtonCodeHelper(self):
        self.codeString = ''
        self.lastFilter='Chrome Dinosaur Game'
        self.initializeSlider()
        file = open(r'assets/codeSamples/chromeDinosaurGame.txt')
        for line in file:
            self.codeString = self.codeString + line
        global codeString
        codeString = self.codeString
        file.close()

    def encryptionCodeHelper(self):
        self.codeString = ''
        self.lastFilter = 'Encryption'
        self.initializeSlider()
        file = open(r'assets/codeSamples/encryptionCode.txt')
        for line in file:
            self.codeString = self.codeString + line
        global codeString
        codeString = self.codeString
        file.close()

    def mainCodeHelper(self):
        self.codeString = ''

        file = open(r'assets/codeSamples/mainCode.txt')
        for line in file:
            self.codeString = self.codeString + line
        global codeString
        codeString = self.codeString
        file.close()

    def thesholdCodeHelper(self):
        self.codeString = ''
        file = open(r'assets/codeSamples/thresholdCode.txt')
        for line in file:
            self.codeString = self.codeString + line
        global codeString
        codeString = self.codeString
        file.close()

    def imageProcessingCodeHelper(self):

        self.codeString = ''
        file = open(r'assets/codeSamples/imageProcessingTransforms.txt')
        for line in file:
            self.codeString = self.codeString + line
        global codeString
        codeString = self.codeString
        file.close()
    def encrpytVideoCodeHelper(self):
        self.lastFilter = 'Video Encryption'
        self.initializeSlider()
        self.codeString = ''
        file = open(r'assets/codeSamples/videoEncryption.txt')
        for line in file:
            self.codeString = self.codeString + line
        global codeString
        codeString = self.codeString
        file.close()
    # End of helper functions

    def createMenuBar(self):

        self.setMinimumHeight(604)
        self.setMinimumWidth(741)
        self.setAutoFillBackground(True)
        exitButton = QAction(QIcon('exit.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        self.mainMenu.addAction(exitButton)
        self.show()

    @pyqtSlot()
    def mainMenuClicked(self):
        self.filterFlag = int(
            0)  # since there were too many if else, I sought to divide the filters into 2 parts. More parts will be
        # added soon , so Its best to keep it this was

        self.actionLoad.triggered.connect(self.loadClicked)
        self.actionSave.triggered.connect(self.saveClicked)
        self.actionExit.triggered.connect(
            self.close)  # These functions are kept to provide professional look to the application.
        self.actionDilate.triggered.connect(self.dilate)
        self.actionErode.triggered.connect(self.erode)
        self.actionMorphological_Gradient.triggered.connect(self.morphGradient)
        self.actionTop_Hat.triggered.connect(self.topHat)
        self.actionBlack_Hat.triggered.connect(self.blackHat)
        self.actionClosing.triggered.connect(self.closing)
        self.actionOpening.triggered.connect(self.opening)

    # Display code in .py File
    def openCodeInPython(self):
        pass

    # play button code
    def displayMessage(self, message):
        print(message)

    # play button, links to the chrome dinasour game
    def playButtonClicked(self):
        self.playButtonCodeHelper() # Helps in displaying code on getCode() Button

        new = 2
        url = 'http://www.trex-game.skipser.com/'
        webbrowser.open(url, new)
        # run the
        message = 'To play the game, put your hand into the frame. Every time you open your hand it simulates a space ' \
                  'pressed. So you can play the chrome dinasour game '
        self.displayMessage(message)
        # ChromeDinasourGame.action()
        ChromeDinasourGamePakhi.action()

    # video load option to allow users to load and apply filters on videos as well
    def loadVideoButtonClicked(self):
        fname, filter = QFileDialog.getOpenFileName(self, 'Open File', '', 'Video Files (*.avi *.mp4 *.mpeg)')
        self.stopVideo = False
        # fname='video.avi'
        if fname:
            cap = cv2.VideoCapture(fname)
            while (cap.isOpened()):
                ret, frame = cap.read()
                if ret == False:
                    print('Video Ended')
                    break
                # print('video')
                # print(frame)
                if (self.lastFilter):
                    self.filterApply(self.lastFilter)
                    self.originalImage = self.processedImage.copy()
                else:
                    print('No Filter')

                self.processedImage = frame.copy()
                self.originalImage = frame.copy()
                self.filterApply(self.lastFilter)
                self.displayImage(2)
                k = cv2.waitKey(40) & 0xFF
                cv2.imshow('Video', self.processedImage)
                if k == ord('q') or k == ord('Q'):
                    break
                elif self.stopVideo:
                    break

            cap.release()
            cv2.destroyAllWindows()
            self.processedImage = self.originalImage.copy()
            self.displayImage()

    def stopVideoButtonClicked(self):
        self.stopVideo = True

    # Rotate Button clicked connect
    def rotateButtonRightClicked(self):
        rows, cols = self.processedImage.shape

        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -90, 2)
        # THIS IS COUNTER CLOCKWISE AND +90 IS CLOCKWISE
        self.processedImage = cv2.warpAffine(self.processedImage, M, (cols, rows))
        self.processedImage = cv2.warpAffine(dst, M, (cols, rows))

        cv2.imshow('Target', dst)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # Rotate Code End

    # Slider Code!
    # slider helper function
    def initializeSlider(self, s=1, e=21):
        self.slider.setRange(s, e)
        if self.slider.value() > e or self.slider.value() < s:
            self.slider.setValue((s + e) / 2)
        self.lineEditSliderValue.setText(str(self.slider.value()))
        self.displayFilter.setText(self.lastFilter)

    # Slider Clicked(Signal Encoded)
    @pyqtSlot()
    def sliderClicked(self):
        # print('Slider Clicked',self.lastFilter)
        if self.filterFlag == int(0):
            if self.lastFilter == 'dilate':
                self.dilate()
            elif self.lastFilter == 'erode':
                self.erode()
            elif self.lastFilter == 'opening':
                self.opening()
            elif self.lastFilter == 'closing':
                self.closing()
            elif self.lastFilter == 'morphGradient':
                self.morphGradient()
            elif self.lastFilter == 'topHat':
                self.topHat()
            elif self.lastFilter == 'blackHat':
                self.blackHat()
            elif self.lastFilter == 'ColorSwap':
                self.filterApply('ColorSwap')
            elif self.lastFilter == 'Moziac':
                self.filterApply('Moziac')
            elif self.lastFilter == 'Canny':
                self.filterApply('Canny')
            elif self.lastFilter == 'Grayscale':
                self.filterApply('Grayscale')
            elif self.lastFilter == 'GaussianBlur':
                self.filterApply('GaussianBlur')
            elif self.lastFilter == 'MedianFilter':
                self.filterApply('MedianFilter')
            elif self.lastFilter == 'BilateralFilter':
                self.filterApply('BilateralFilter')
            elif self.lastFilter == 'Geometric 1':
                self.filterApply('Geometric 1')

        elif self.filterFlag == int(1):
            # apply thresholds only
            if self.lastFilter == 'BinaryThreshold':
                self.threshold('BinaryThreshold')
            elif self.lastFilter == 'BinaryInverseThreshold':
                self.threshold('BinaryInverseThreshold')
            elif self.lastFilter == 'TruncThreshold':
                self.threshold('TruncThreshold')
            elif self.lastFilter == 'TozeroThreshold':
                self.threshold('TozeroThreshold')
            elif self.lastFilter == 'TozeroThresholdInverse':
                self.threshold('TozeroThresholdInverse')
            elif self.lastFilter == 'AdaptiveThreshold_Mean_C':
                self.threshold('AdaptiveThreshold_Mean_C')
            elif self.lastFilter == 'AdaptiveThreshold_Gaussian':
                self.threshold('AdaptiveThreshold_Gaussian')
            elif self.lastFilter == 'OtsuThreshold':
                self.threshold('OtsuThreshold')
        elif self.filterFlag == 2:
            if self.lastFilter == 'DetectContours':
                self.applyImageProcessingHelper('DetectContours')
            elif self.lastFilter == 'PrintCurrentContours':
                self.applyImageProcessingHelper('PrintCurrentContours')
        elif self.filterFlag == 3:
            if self.lastFilter == 'ShiThomsiCornerDetection':
                self.applyCornerDetectionHelper('ShiThomsiCornerDetection')

            elif self.lastFilter == 'harrisonCornerDetection':
                print('here')
                self.applyCornerDetectionHelper('harrisonCornerDetection')

            elif self.lastFilter == 'FASTCornerDetection':
                self.applyImageProcessingHelper('FASTCornerDetection')
        elif self.filterFlag == 4:
            pass
            # if self.lastFilter == 'DetectContours':
            #     self.applyImageProcessingHelper('DetectContours')
            # elif self.lastFilter == 'PrintCurrentContours':
            #     self.applyImageProcessingHelper('PrintCurrentContours')

    @pyqtSlot()
    def lineEditSliderValueClicked(self):
        print('In lineEditSlider')
        if self.lastFilter == 'No Filter Used':
            # No filter was used.
            return
        self.slider.setValue(int(self.lineEditSliderValue.text()))
        self.initializeSlider()
        self.sliderClicked()

    # Slider Code Clicked End

    # Close(1 line)
    def close(self):
        sys.exit(app.exec_())

    # Instructions and About Code
    @pyqtSlot()
    def instructionClicked(self):
        message = 'Applications: \n' \
                  'Paint Application, brush resizing, brush color and saving' \
                  '\n Load Video, Save Video\n' \
                  'Encryption and Decryption of code in Images and Videos' \
                  '\n Filters on Videos\n' \
                  ''
        QMessageBox.about(self, "Photoshop : Instructions", message)

    @pyqtSlot()
    def aboutClicked(self):
        message = 'Authored and Made By Team Vision. This was made as a part of GUI development, implementing ' \
                  'machine learning algorithms and making the Open CV easy to understand.\n\n' \
                  'Reach Out to teamVision:\n\nGithub: https://github.com/ashishgupta1350/teamVision \n\nLinkedin: ' \
                  ' \n\nSpecial Thanks to : Dave Gandy (' \
                  'https://www.flaticon.com/authors/dave-gandy) for cool icons '
        QMessageBox.about(self, "Photoshop", message)

    # Saved Clicked
    @pyqtSlot()
    def saveClicked(self):
        print('save Clicked')

        fname, filter = QFileDialog.getSaveFileName(self, 'Save File', '', 'Image Files (*.png *.xpm *.jpg)')
        if fname:
            cv2.imwrite(fname, self.processedImage)
        else:
            print('Not Saved')


    # Most important function using QPixMap

    def displayImage(self, windowName=1):  # window name is for future reference

        qformat = QImage.Format_Indexed8

        if len(self.processedImage.shape) == 3:  # rows cols and color channel.
            if self.processedImage.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(self.processedImage, self.processedImage.shape[1], self.processedImage.shape[0],
                     self.processedImage.strides[0], qformat)
        # print(flag)

        img = img.rgbSwapped()  # RGB to BGR to display(basic)
        # no need for window Name, added as a precautionary statement for further advancements in features

        if windowName == 1:
            self.imageLabel.setPixmap(QPixmap.fromImage(img))
            self.imageLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.imageLabel.setScaledContents(1)

        else:
            self.imageLabel.setPixmap(QPixmap.fromImage(img))
            self.imageLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.imageLabel.setScaledContents(1)

    # Update Original Image
    @pyqtSlot()
    def updateOriginalImage(self):
        print('Updated Original')
        self.originalImage = self.processedImage.copy()
        # self.image = self.originalImage

    # Reset Image
    @pyqtSlot()
    def resetClicked(self):
        print('Reset Clicked')
        self.processedImage = self.originalImage.copy()
        self.displayImage(2)

    # Load Clicked
    @pyqtSlot()
    def loadClicked(self):
        print('Load Clicked')

        fname, filter = QFileDialog.getOpenFileName(self, 'Open File', '', 'Image Files (*.png *.xpm *.jpg)')
        if fname:
            self.loadImage(fname)
        else:
            print('Invalid Image')  # print some sort of information box?? Not necessarily

    def loadImage(self, fname):
        print('Load Image')
        if fname:
            self.originalImage = cv2.imread(fname)
            # self.image = cv2.imread(fname)
            self.processedImage = self.originalImage.copy()  # for future
            self.displayImage(1)
        else:
            print('No image was loaded')

    # ---------------------- Code for Morphological Transforms Was Here Before Refactoring ------------------- #

    # code shifted to file via decorators

    # Morphological code ends

    # IP cam Code for Mobile Imaging

    def open_new_dialog(self):
        self.nd = IPCamDialog(self)
        self.nd.show()

    def loadVideoFromMobile(self):

        # Replace the URL with your own IPwebcam shot.jpg IP:port

        ex = IPCamDialog(self)
        print('IP set as : ', IPCamURL)

    def loadVideoFromMobileHelper(self):
        # url = 'http://192.168.1.5:8080/shot.jpg'
        # url = IPCamURL.copy()
        print('Here')
        url = IPCamURL
        print(IPCamURL)
        print('Here')

        print('To edit any image, press s to load the image to the main console and press q to quit!')
        cv2.namedWindow('IPCamera', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('IPCamera', 800, 600)
        while True:

            # Use urllib to get the image from the IP camera
            try:
                imgResponse = urllib.request.urlopen(url)
            except:
                print('The IP cam is not connected, please connect it first!')
                break
            print('here')
            # Numpy to convert into a array
            imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)

            # Decode the array to OpenCV usable format
            img = cv2.imdecode(imgNp, -1)

            # put the image on screen
            cv2.imshow('IPCamera', img)

            k = cv2.waitKey(1) & 0xFF
            if k == ord('q') or k == 27:
                break

            elif k == ord('s'):
                img = cv2.pyrDown(img)
                self.processedImage = img.copy()
                self.originalImage = img.copy()
                self.displayImage(2)
                # this does not do anything to original image so reset feature is still enabled
                print('Image now available of main screen editing')

        cv2.destroyAllWindows()


    def faceBlur(self):
        image = self.processedImage.copy()
        gray = image
        if len(image.shape) >= 3:
            # Convert the image to RGB colorspace
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Convert the RGB  image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Extract the pre-trained face detector from an xml file
        face_cascade = cv2.CascadeClassifier('detector_architectures/haarcascade_frontalface_default.xml')

        # Detect the faces in image
        faces = face_cascade.detectMultiScale(image, 1.3, 5)
        # Print the number of faces detected in the image
        print('Number of faces detected:', len(faces))

        # Make a copy of the orginal image to draw face detections on
        image_with_detections = np.copy(image)

        face_crop = faces
        # Get the bounding box for each detected face

        result_image = image.copy()
        try:
            for (x, y, w, h) in faces:
                # Add a red bounding box to the detections image
                cv2.rectangle(image_with_detections, (x, y), (x + w, y + h), (255, 0, 0), 3)
                face_crop = image_with_detections[y:y + h, x:x + w]
                ## Blur the bounding box around each detected face using an averaging filter and display the result
                kernel_2 = np.ones((40, 40), np.float32) / 1600
                blur_2 = cv2.filter2D(face_crop, -1, kernel_2)
                print("here")

                result_image[y:y + blur_2.shape[0], x:x + blur_2.shape[1]] = blur_2
        except:
            print('Unable to detect any face')

        self.processedImage = result_image.copy()
        self.displayImage(2)

    def detectFace(self):

        face_cascade = cv2.CascadeClassifier('detector_architectures/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('detector_architectures/haarcascade_eye.xml')

        img = self.processedImage.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        roi_color = img
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        self.processedImage = img.copy()
        self.displayImage(2)

    def detectFaceOnly(self):
        face_cascade = cv2.CascadeClassifier('detector_architectures/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('detector_architectures/haarcascade_eye.xml')

        img = self.processedImage.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        roi_color = img
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            
        self.processedImage = img.copy()
        self.displayImage(2)


    def applyFacialFiltersHelper(self, currentTool):

        self.processedImage = self.originalImage.copy()

        if currentTool == 'FaceBlur':

            print('\n\nFace Blur Called, usage: blurs all the faces')
            self.lastFilter = 'FaceBlur'
            self.initializeSlider(s=20, e=255)
            self.faceBlur()

        elif currentTool == 'FaceAndEyeDetection':
            print('\n\nFace and Eye Detection Called')
            self.lastFilter = 'FaceAndEyeDetection'
            self.initializeSlider(s=20, e=255)
            self.detectFace()

        elif currentTool == 'FaceDetection':
            print("\n\nFace Detection Called")
            self.lastFilter = 'Face Detection'
            self.initializeSlider(s=20,e=255)
            self.detectFaceOnly()

    def applyFacialFilters(self):
        self.filterFlag = 4
        currentTool = self.faceQComboBox.currentText()
        self.applyFacialFiltersHelper(currentTool)



app = QApplication(sys.argv)
window = gui()
window.setWindowTitle('Photoshop - Team Vision')
window.show()
sys.exit(app.exec_())

