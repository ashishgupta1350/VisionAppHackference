## Image Encryption, watermark, etc code starts .


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
    from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox, QAction, QMainWindow
except:
    print("Please install PyQt5 first to run the interface!")
    exit(1)

try:
    import matplotlib.pyplot as plt
except:
    print('Please install matplotlib, some features like [Histograms] will not work')


def getChar(self, binChar):
    binChar = reversed(binChar)
    mul = int(1)
    sum = int(0);
    for i in binChar:
        sum += (ord(i) - ord('0')) * mul
        mul *= int(2)
    return str(chr(sum))


def getNumFromBin(self, binaryThing):
    binaryThing = reversed(binaryThing)
    mul = int(1)
    sum = int(0);
    for i in binaryThing:
        sum += (ord(i) - ord('0')) * mul
        mul *= int(2)
    return sum


def binary2String(self, myBinString):
    i = 0
    #     myBinString='01100001'
    retString = ''
    l = len(myBinString)
    while i < l:
        binChar = myBinString[i:i + 8]
        ch = self.getChar(binChar)
        retString += ch
        i += 8;
    return retString


def string2Binary(self, myString):
    # myString = 'This is me'
    binString = ''
    for i in myString:
        a = ord(i)
        bitstring = bin(a)
        bitstring = bitstring[2:]
        bitstring = -len(bitstring) % 8 * '0' + bitstring
        binString += bitstring
    return binString


def waterMarkImageClicked(self, watermark=' This Image is Encrypted! '):
    # iterate over the matrix channel 1 and change some of the values.

    self.encryptionCodeHelper()

    self.lastFilter = 'Image Encryption'
    self.initializeSlider()

    print('Encrypting:')
    rows = 0
    cols = 0
    channel = 0
    if not watermark:
        watermark = ' This Image is Encrypted '  # rarest of the rare case, that they ever come together in a random
        # Image.

    index = 0
    watermarkBin = self.string2Binary(watermark)
    if len(self.processedImage.shape) == 2:
        rows, cols = self.processedImage.shape
    else:
        rows, cols, channel = self.processedImage.shape
    # for stopping once the file has ended so that I dont apply watermark again and again and again( if the water
    #  mark is appended with the end of file string)
    if len(self.processedImage.shape) == 2:
        index = 0
        for row in range(rows):
            for col in range(cols):

                num = self.processedImage[row][col]
                # convert the num to binary
                bitstring = bin(num)
                bitstring = bitstring[2:]
                bitstring = -len(bitstring) % 8 * '0' + bitstring
                # after converting it to binary change the last positions of the image number
                temp = bitstring[0:6]
                if index + 1 < len(watermarkBin):
                    temp += watermarkBin[index:index + 2]
                    index += 2
                else:
                    index = 0
                index = index % len(watermarkBin)
                self.processedImage[row][col] = self.getNumFromBin(temp)


    elif len(self.processedImage.shape) == 3:
        index = 0
        for row in range(rows):
            for col in range(cols):

                num = self.processedImage[row][col][0]
                # convert the num to binary
                bitstring = bin(num)
                bitstring = bitstring[2:]
                bitstring = -len(bitstring) % 8 * '0' + bitstring
                temp = ''
                temp += bitstring[0:6]
                # after converting it to binary change the last positions of the image number, the green channel has
                # all the data
                if index + 1 < len(watermarkBin):
                    temp += watermarkBin[index]
                    temp += watermarkBin[index + 1]
                    index += 2
                else:
                    index = 0

                index = index % len(watermarkBin)
                self.processedImage[row][col][0] = self.getNumFromBin(temp)

    if len(self.processedImage.shape) > 0:
        self.displayImage(2)
        print('WaterMarked! Click Update original and then save to save this encrypted image on disk.')


# newest function in the line
def encryptImageHelper(self, data):
    # iterate over the matrix channel 1 and change some of the values.

    self.encryptionCodeHelper()

    self.lastFilter = 'Image Encryption'
    self.initializeSlider()
    data += '\n\n!@#$%^&*'  # this is faster than normal and there is a very low chance of getting this in any
    # expression continuously!
    print('Encrypting:')
    rows = 0
    cols = 0
    channel = 0
    myEndFlag = 0
    if not data:
        data = ' This Image is Encrypted '  # rarest of the rare case, that they ever come together in a random Image.

    binaryData = self.string2Binary(data)  # convert the data to binary
    if len(self.processedImage.shape) == 2:
        rows, cols = self.processedImage.shape
    else:
        rows, cols, channel = self.processedImage.shape
    # for stopping once the file has ended so that I dont apply watermark again and again and again( if the water
    #  mark is appended with the end of file string)
    if len(self.processedImage.shape) == 2:
        index = 0
        for row in range(rows):
            for col in range(cols):

                num = self.processedImage[row][col]
                # convert the num to binary
                bitstring = bin(num)
                bitstring = bitstring[2:]
                bitstring = -len(bitstring) % 8 * '0' + bitstring
                # after converting it to binary change the last positions of the image number
                temp = bitstring[0:6]
                if index + 1 < len(binaryData):
                    temp += binaryData[index:index + 2]
                    index += 2
                else:
                    index = 0
                    self.processedImage[row][col] = self.getNumFromBin(temp)
                    myEndFlag = 1
                    break

                # index = index % len(binaryData) # we dont want to do that the index circles around the image.
                # Instread we want to break it.
                self.processedImage[row][col] = self.getNumFromBin(temp)
            if myEndFlag == 1:
                break

    elif len(self.processedImage.shape) == 3:
        index = 0
        for row in range(rows):
            for col in range(cols):

                num = self.processedImage[row][col][0]
                # convert the num to binary
                bitstring = bin(num)
                bitstring = bitstring[2:]
                bitstring = -len(bitstring) % 8 * '0' + bitstring
                temp = ''
                temp += bitstring[0:6]
                # after converting it to binary change the last positions of the image number, the green channel has
                # all the data
                if index + 1 < len(binaryData):
                    temp += binaryData[index]
                    temp += binaryData[index + 1]
                    index += 2
                else:
                    index = 0
                    self.processedImage[row][col] = self.getNumFromBin(temp)
                    myEndFlag = 1
                    break

                # index = index % len(binaryData)
                self.processedImage[row][col][0] = self.getNumFromBin(temp)
            if myEndFlag == 1:
                break

    if len(self.processedImage.shape) > 0:
        self.displayImage(2)
        print('WaterMarked! Click Update original and then save to save this encrypted image on disk.')


def bringEncryptedDataFromImage(
        self):  # is data flag was true , then the function stores data else it stores the watermark only.

    self.encryptionCodeHelper()

    print('Decrypting the Image :\n')
    rows = 0
    cols = 0
    channel = 0
    index = 0
    # checks the end of the data stream.
    endChecker = ''
    dataFromImage = ''  # this will contain a binary string that will be read from the image
    dataFromImageReturn = ''
    if len(self.processedImage.shape) == 2:
        rows, cols = self.processedImage.shape
    else:
        rows, cols, channel = self.processedImage.shape
    # tempFlag = False
    timeToReturn = False  # returns if it detects that the endOfFile we added to the image at encryption >> !@#$%^&*

    if len(self.processedImage.shape) == 2:
        for row in range(rows):
            for col in range(cols):
                num = self.processedImage[row][col]
                # convert the num to binary
                bitstring = bin(num)
                bitstring = bitstring[2:]
                bitstring = -len(bitstring) % 8 * '0' + bitstring
                # after converting it to binary change the last positions of the image number
                dataFromImage += bitstring[6:8]
                dataFromImageReturn += bitstring[6:8]
                if len(dataFromImage) >= 8:  # to check the end of the file statement from data flag
                    if len(endChecker) == 7:
                        if endChecker == '!@#$%^&':
                            timeToReturn = True
                            break
                        else:
                            endChecker = endChecker[1:]
                            endChecker += self.binary2String(dataFromImage)
                    elif len(endChecker) < 7:
                        endChecker += self.binary2String(dataFromImage)
                    else:
                        endChecker = ''
                    print(self.binary2String(dataFromImage), end='')
                    dataFromImage = ''
            if timeToReturn:
                break
    elif len(self.processedImage.shape) == 3:
        for row in range(rows):
            for col in range(cols):
                num = self.processedImage[row][col][0]
                # convert the num to binary
                bitstring = bin(num)
                bitstring = bitstring[2:]
                bitstring = -len(bitstring) % 8 * '0' + bitstring
                # after converting it to binary change the last positions of the image number
                dataFromImage += bitstring[6:8]
                dataFromImageReturn += bitstring[6:8]

                if len(dataFromImage) >= 8:  # to check the end of the file statement from data flag
                    if len(endChecker) == 7:
                        if endChecker == '!@#$%^&':
                            timeToReturn = True
                            break
                        else:
                            endChecker = endChecker[1:]
                            endChecker += self.binary2String(dataFromImage)
                    elif len(endChecker) < 7:
                        endChecker += self.binary2String(dataFromImage)
                    else:
                        endChecker = ''
                    print(self.binary2String(dataFromImage), end='')
                    dataFromImage = ''
            if timeToReturn:
                break

    print('\n\nThe Image was Successfully Scanned!')
    # so I got the watermark, now time to print the watermark!
    # print(self.binary2String(imageWatermark[:]))
    return self.binary2String(dataFromImageReturn)[:-8]


def checkWatermark(
        self):  # is data flag was true , then the function stores data else it stores the watermark only.

    self.encryptionCodeHelper()

    print('WaterMarking /Decrypting the Image:')
    rows = 0
    cols = 0
    channel = 0
    index = 0
    imageWatermark = ''  # this will contain a binary string that will be read from the image
    imageWatermarkReturn = ''
    if len(self.processedImage.shape) == 2:
        rows, cols = self.processedImage.shape
    else:
        rows, cols, channel = self.processedImage.shape
    # tempFlag = False
    if len(self.processedImage.shape) == 2:
        for row in range(rows):
            for col in range(cols):
                num = self.processedImage[row][col]
                # convert the num to binary
                bitstring = bin(num)
                bitstring = bitstring[2:]
                bitstring = -len(bitstring) % 8 * '0' + bitstring
                # after converting it to binary change the last positions of the image number
                imageWatermark += bitstring[6:8]
                imageWatermarkReturn += bitstring[6:8]
                if len(imageWatermark) >= 8:  # to check the end of the file statement from data flag
                    print(self.binary2String(imageWatermark), end='')
                    imageWatermark = ''

    elif len(self.processedImage.shape) == 3:
        for row in range(rows):
            for col in range(cols):
                num = self.processedImage[row][col][0]
                # print('here')
                # convert the num to binary
                bitstring = bin(num)
                bitstring = bitstring[2:]
                bitstring = -len(bitstring) % 8 * '0' + bitstring
                # after converting it to binary change the last positions of the image number
                # imageWatermark+=bitstring[6:8]
                imageWatermark += bitstring[6:8]
                imageWatermarkReturn += bitstring[6:8]

                # if len(imageWatermark) >= 8:  #old working code without end of the file
                #     print(self.binary2String(imageWatermark),end='')
                #     imageWatermark=''
                if len(imageWatermark) >= 8:  # to check the end of the file statement from data flag
                    print(self.binary2String(imageWatermark), end='')
                    imageWatermark = ''

    print('\n\nThe image was successfully scanned')

    # so I got the watermark, now time to print the watermark!
    # print(self.binary2String(imageWatermark[:]))
    return self.binary2String(imageWatermarkReturn)


def encryptDataClicked(self):

    self.encryptionCodeHelper()

    fname, _ = QFileDialog.getOpenFileName(self, 'Open Text File', '', 'Text File (*.txt)')
    data = None
    myfile = None
    try:
        if fname:
            with open(fname, encoding="utf8", errors='ignore') as myfile:
                data = myfile.read()
                data=str(data)
                # print(data)
            # self.waterMarkImageClicked(data)
            self.encryptImageHelper(data)
            myfile.close()
        else:
            print("Please reselect a valid file!")
    except Exception as e:
        print(e)
        print("Invalid file format and/or you need to input a text file")
        print("")



def decryptDataClicked(self):
    self.encryptionCodeHelper()

    print('Decrypting: ')
    fname, _ = QFileDialog.getOpenFileName(self, 'Open File to save', '', 'Text File (*.txt)')
    data = None
    myfile = None

    if fname:
        with open(fname, 'w') as myfile:
            # myfile.write(self.checkWatermark())
            myfile.write(self.bringEncryptedDataFromImage())
        myfile.close()
    else:
        print('Please reselect a valid file!')


## Image Encryption code ends


# This is the functions for the decorators in the main file of Photoshop. This can be used to send functions to the
# main file!
functions = (getChar, getNumFromBin, binary2String, string2Binary, waterMarkImageClicked, encryptImageHelper,
             bringEncryptedDataFromImage, checkWatermark, encryptDataClicked, decryptDataClicked)
