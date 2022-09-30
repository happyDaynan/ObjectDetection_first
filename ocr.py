import os, cv2, pytesseract, imutils 
import numpy as np



def octimge(filePath):
    
    cap = cv2.VideoCapture(filePath)  

    

    while True:
        ret, frame = cap.read()

        frame = frame[20: 50, 1070:1245] #ipcamer07 時間影像位置
        frame = imutils.resize(frame, width = 320)

        gray =  cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        thresholding = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        kernel = np.ones((2,2),np.uint8)   
        open = cv2.morphologyEx(thresholding, cv2.MORPH_OPEN, kernel)
        close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel)
        canny =  cv2.Canny(close, 300, 500)

        dilatekernel = np.ones((5,5),np.uint8)
        dilate = cv2.dilate(canny, dilatekernel, iterations = 1)
        erodekernel = np.ones((3,3),np.uint8)
        erode = cv2.erode(dilate, erodekernel, iterations = 2)

        cv2.imshow('frame', frame)
        cv2.imshow('dilate',dilate)
        cv2.imshow('thresholding', thresholding)
        cv2.imshow('erode', erode)
        cv2.imshow('canny', canny)

        if cv2.waitKey(1) & 0xFF == ord('q'): # 按Q            

            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    myPath = "./testervideo/001.mp4"

    octimge(myPath)

