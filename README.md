# VisionAppHackference
Vision App( Photoshop ) is what Arduino is to microcontrollers.

### Summary
Vision app is a GUI based scalable app that facilitates learning and application of image and video processing without knowing any mathematics and writing a single line of code. Vision app allows application of OpenCV filters from 3- 5 minutes to 2 seconds and helps students (even children) learn and apply image processing on the go. Vision app is also a module oriented platform that allows addition of cloud, cryptography and server modules to be added.


### Problems answered
The barrier to entry in the field of image processing is very high. For doing image processing, knowledge to python is not enough, rather far for it. You should know Mathematics and 100's of parameters passed to function. Not just that, you need to have solid command over virtual environments, python pip, numpy, matplotlib to draw images. In short, for a non engineer, it is practiacally very hard or infeasable. 

A problem that comes with researchers is reaplication of 100's of lines of code to get the correct filter they want. If you are a researcher who is looking to isolate number plate from image, you need to know Canny Edge detection and 5 paramers that come along. Vision App reduces that to no code. 

The problem with children is no familiarity with mathematics and python (advanced). Vision app makes impossible possible.
Problem with developers is that they have to know the entire opencv framework. So if as a developer, one wants to implement a tensorflow code into the application using opencv, one has to code in Tensorflow, import dependencies in python, install and import opencv, write the opencv code to see the algorithm working. This seems like a usual way, but how about providing a interface with all the dependencies preinstalled ? Also, you have to vary your code from platform to platform, from Ipython notebook to python in ios to jetbrains in Ubuntu. Why not remote this?

### Extentions ( It goes beyond Photoshop and Adobe after effects, all with 20 hrs of coding and code integration )

Vision app goes beyond photoshop. What if you have to apply for 100s of images. You can make a video of 100's of images and run filters on videos in real time. One can stop anytime and apply filters on any desired frame as well. All of this happens using parallel processing on threads.

Vision app is module oriented, just like android apps extend android, one can add code to Vision app like installing "Google Chrome" on windows. 3 lines of code and done! You can add any module. We have added 4 modules ( just like apps on Google Play) to this application
1) Cryptography to input entire books into video of few seconds. We encoded "harry potter and the sorcers stone book" in 0.2 seconds of video. For every 10 mb of video, one can add 2 mbs of books ( 10-20 books). 

2) IP Cam for applying filters from images in real time over a local server using  android, Cynogen OS etc. So processing images does not required pushing images to cloud from phone and then downloading them to use filters. Filters are applied in real time.

3) Get code feature allows to get code for applied feature that can copied and run the same code that was applied. The students and even children under 15 years can easily code 100's of lines of complicated code with basic knowledge of python.

5) Game using hand gesture recognition. With one click, one can play Chrome dinosour game using hands, right on the browser.

Vision app is cross platform application. It runs on all the  runs on Windows, Linux and Mac Os! The gui is resizable. The code uses parallel processing and error resiliant.



### Features
Image enryption
Image Processing on:
1) Images
2) Videos
3) Camera Feed
4) IOT device live feeds

Cryptography
Gesture Recognition Game

### Modules
Cryptography
Gesture Recognition Game
IP Cam
Get Going With Code!

Images:




# Install instructions:

### Pycharm

```
Install pycharm
Download the zip project and extract it.
Open the project in Pycharm
In pycharm, go to file >> settings >> (projectname) >> project interpreter
Add project interpreter (Python Version 3.5+ will work only. Try installing conda with python 3.6 or 3.7 and porting the compiller from there )
On the right hand side, click the + button.

Install the following repositories in the menu
1) Opencv
2) Numpy ( comes with open cv)
3) Matplotlib
4) xlib-python
5) PyQt5
6) PyautoGUI

That's it.
Go the the photoshop.py to run the code
```

### Without pycharm

```
install virtualenv
Run a virtual environment ( Link : https://www.geeksforgeeks.org/python-virtual-environment/ )
install opencv
install numpy
install matplotlib
install xlib
install PyQt5
install pyautogui

that's it. Now the run photoshop.py using env's python interpretter.
```

Note: Tested for Ubuntu and Windows. Mac is not tested. Kindly verify and reach out to us for MAC.

Note: Links to installation
```
1) Install pycharm
https://medium.com/@GalarnykMichael/setting-up-pycharm-with-anaconda-plus-installing-packages-windows-mac-db2b158bd8c
2) Install opencv
https://www.learnopencv.com/install-opencv3-on-ubuntu/
https://www.learnopencv.com/install-opencv3-on-windows/

3) matplotlib
https://matplotlib.org/users/installing.html
4) xlib
https://github.com/python-xlib/python-xlib
5) numpy
http://www.numpy.org/
https://www.geeksforgeeks.org/numpy-in-python-set-1-introduction/
6) Pyqt5
https://pythonspot.com/pyqt5/
7) pyautoGUI
https://pyautogui.readthedocs.io/en/latest/
```



