##  Face Detection Code Start  ##
import cv2

def actionFaceDetectionClicked(self, detectEye=1):
    # print('Face Detection:')
    self.lastFilter = 'FaceDetection'
    self.initializeSlider()

    tempImage = self.processedImage.copy()  # local Image
    gray = None
    if len(tempImage.shape) >= 3:
        gray = cv2.cvtColor(tempImage, cv2.COLOR_BGR2GRAY)
    else:
        gray = tempImage.copy()
    faces = self.face_cascade.detectMultiScale(gray, 1.3, 7)  # test the 1.3 with the slider please
    if len(faces) == 0:
        return
    if self.detectEye.isChecked() == False:
        detectEye = 2
    else:
        detectEye = 1
    for (x, y, w, h) in faces:
        cv2.rectangle(tempImage, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # cut a roi on the faces
        roi_color = tempImage[y:y + h, x:x + w]
        roi_gray = gray[y:y + h, x:x + y]
        if (detectEye == 1):
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 255), 2)

    self.processedImage = tempImage.copy()
    self.displayImage(2)

## Face Detection Code End  ##

functions = (actionFaceDetectionClicked,)


