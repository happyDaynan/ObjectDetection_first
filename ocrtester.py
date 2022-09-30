import os
import pytesseract
from PIL import Image
import numpy as np
import cv2



def main():

    """
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    img = Image.open(r"testimg\002.jpg")
    img.show()
    print(pytesseract.image_to_string(img, lang="eng"))
    """
    
    #imgpath = r"testimg\output_0001.JPG"
    #imgpath = r"testimg\output_0000.JPG"
    imgpath = r"testimg\002.JPG"

    readimg = cv2.imread(imgpath, cv2.IMREAD_COLOR)

    # 調整大小
    res_img = cv2.resize(readimg, (800, 800), interpolation=cv2.INTER_CUBIC)

    # 灰階
    grayimg = cv2.cvtColor(readimg, cv2.COLOR_RGB2GRAY)

    cv2.imshow('Image', grayimg)
    cv2.waitKey(0)
    
    # 二值化反轉
    sim_inv = cv2.threshold(grayimg, 110, 255, cv2.THRESH_BINARY_INV)[1]

    cv2.imshow('Image', sim_inv)
    cv2.waitKey(0)
    
    # 模糊化
    # mblur = cv2.medianBlur(sim_inv, 5)

    #cv2.imshow('Image', mblur)
    # cv2.waitKey(0)

    # 開運算
    kernel = np.ones((2,2), np.uint8)
    open_img = cv2.morphologyEx(grayimg, cv2.MORPH_OPEN, kernel)
  

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    imgtostr = pytesseract.image_to_string(open_img, lang="eng")

    print(imgtostr)



# IPCamera07
def ipcamer07(imgpath):

    readimg = cv2.imread(imgpath, cv2.IMREAD_COLOR)

    # 拍攝時間
    datetime_x1, datetime_x2 = 1070, 1280
    datetime_y1, datetime_y2 = 0, 100
    datetime_img = readimg[datetime_y1: datetime_y2, datetime_x1: datetime_x2]


    # 機器名稱 
    machinename_x1, machinename_x2 = 0, 300
    machinename_y1, machinename_y2 = 650, 800
    machinename_img = readimg[machinename_y1: machinename_y2, machinename_x1: machinename_x2]

    datetimestr = ipcamer07getstr(datetime_img)
    machinenamestr = ipcamer07getstr(machinename_img)

    newfilename = f"{machinenamestr}_{datetimestr}.jpg"
    
    return newfilename

    

def ipcamer07getstr(img):

    grayimg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    sim_inv = cv2.threshold(grayimg, 110, 255, cv2.THRESH_BINARY_INV)[1]

    kernel = np.ones((2,2), np.uint8)
    open_img = cv2.morphologyEx(sim_inv, cv2.MORPH_OPEN, kernel)
    open_img = cv2.morphologyEx(open_img, cv2.MORPH_CLOSE, kernel)

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    imgtostr = pytesseract.image_to_string(open_img, lang="eng")


    imgtostr = imgtostr.split(" ")
    imgtostr_len = len(imgtostr)

    # 機器名稱
    if imgtostr_len == 1:

        return imgtostr[0].split("\n")[0]
        
    # 拍攝時間
    if imgtostr_len == 3:
       return imgtostr[0] + imgtostr[1]


    
    
 # 處理 1FAT_29   
def fat_29(imgpath):    

    readimg = cv2.imread(imgpath, cv2.IMREAD_COLOR)

    # 設定裁切範圍
    x1, x2 = 0, 500
    y1, y2 = 0, 30

    date_x1, date_x2  = 1600 , 2000
    date_y1 , date_y2 = 0 , 30

    # 機器名稱圖片
    loc_1 = readimg[y1:y2, x1: x2]

    # 機器拍攝時間圖片
    loc_2 = readimg[date_y1:date_y2, date_x1:date_x2]      


    namestring = getNametime(loc_1)
    timestring = getNametime(loc_2)

    Namestr = f"{namestring}_{timestring}.jpg"   
 
    return Namestr

    


def salt(img, n):
    for k in range(n):
        i = int(np.random.random() * img.shape[1])
        j = int(np.random.random() * img.shape[0])
        if img.ndim == 2:
            img[j,i] = 255
        elif img.ndim == 3:
            img[j,i,0]= 255
            img[j,i,1]= 255
            img[j,i,2]= 255
        return img


# getnameandtime
def getNametime(img): 

    # 灰階
    grayimg = cv2.cvtColor(img , cv2.COLOR_RGB2GRAY)

    # 去躁點
    saltimg = salt(grayimg, 500)
    # 二值化反轉
    sim_inv = cv2.threshold(saltimg, 0, 255, cv2.THRESH_BINARY_INV)[1]

    cv2.imshow('sim_inv', sim_inv)
    cv2.waitKey(0)

    # 
    kernel = np.ones((2,2), np.uint8)
    open_img = cv2.morphologyEx(sim_inv, cv2.MORPH_OPEN, kernel)
    open_img = cv2.morphologyEx(open_img, cv2.MORPH_CLOSE, kernel)

    cv2.imshow('open_img', open_img)
    cv2.waitKey(0)   
    
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # 取文字
    imgstr = pytesseract.image_to_string(open_img, lang="eng")

    imgstr = imgstr.split("\n")[0]
    imgstrlen = len(imgstr)

    # 機器名稱
    if imgstrlen == 7:
       return imgstr
    
    # 拍攝時間
    if imgstrlen == 18:
        
        imgstr = imgstr.split(" ")

        datestr = imgstr[0].split("7")

        # datestr = datestr.split("7")

        timestr = imgstr[1]     

        return datestr[0] + datestr [1] + timestr

        

if __name__ == "__main__":
    
    #imgpath = r"testimg\002.JPG" 
    imgpath = r"./fat_29/002.jpg"


    #ipcamer07
    #impgpath = r"./ipcamera07/output_0000.jpg"
    
    #filename = ipcamer07(impgpath)
    #print(filename)



    # 針對 1fat29
    fileName = fat_29(imgpath)

    print(fileName)
