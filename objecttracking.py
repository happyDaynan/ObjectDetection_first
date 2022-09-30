from fileinput import filename
from posixpath import split
import cv2, os
import numpy as np
import pytesseract
import imutils, time
from datetime import datetime


"""OCR執行檔安裝位置"""
tesseractstr = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# 計算影片長度
def videolen(filePath):

    # https://stackoverflow.com/questions/49048111/how-to-get-the-duration-of-video-using-cv2
    video = cv2.VideoCapture(filePath)
    fps = video.get(cv2.CAP_PROP_FPS) # 每秒的FPS
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT) # 影片的總幀數
    seconds = frame_count / fps
    totaltime = time.strftime('%H:%M:%S', time.gmtime(seconds)) # 影片總時間
    # minutes = int(seconds / 60)
    # rem_sec = int(seconds % 60)
    return totaltime


    


def objectdetection(filePath):

    # Object detection from Stable camera
    object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

    cap = cv2.VideoCapture(filePath)   

    strlist = []
    strlist_2 = []

    while True:

        ret, frame = cap.read()

        # 紀錄時間
        starttime = cv2.getTickCount()

        # 若讀取至影片結尾，則跳出
        if ret == False:
            break


        height, width, _ = frame.shape
        # print(f"{height}, {width}")        

        # Extract Region of interest
        # roi = frame[0: width,0: height]
        frame_1 = frame[20: 50, 1070:1245] #ipcamer07 時間影像位置
        frame_1 = imutils.resize(frame_1, width = 320)

        # frame_2 = frame[0: 20, 1205:1360] #1fat_29 時間影像位置
        # frame_2 = imutils.resize(frame_2, width = 320)
        
        roi = frame #全景

        mask = object_detector.apply(roi) 
        _, mask = cv2.threshold(mask, 245, 255, cv2.THRESH_BINARY) 
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        
        for cnt in contours:

            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            
            # 檢測
            if  area > 500:

                gray =  cv2.cvtColor(frame_1, cv2.COLOR_RGB2GRAY)
                sim_inv = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY_INV)[1]
                

                kernel = np.ones((2,2), np.uint8)
                open_img = cv2.morphologyEx(sim_inv, cv2.MORPH_OPEN, kernel)            
                open_img = cv2.morphologyEx(open_img, cv2.MORPH_CLOSE, kernel)

                pytesseract.pytesseract.tesseract_cmd = tesseractstr

                imgtostr = pytesseract.image_to_string(open_img, lang="eng") 

                                                                      
                            
            


               

              
                                 

                    
        # cv2.imshow('frame', frame)
        cv2.imshow('日期時間', frame_1)
        # cv2.imshow("mask", mask)
        # cv2.imshow("roi", roi)       



        if cv2.waitKey(1) & 0xFF == ord('q'): # 按Q
                        

            break

    cap.release()
    cv2.destroyAllWindows()

    # 影片結束時間
    endtime = cv2.getTickCount()

    

# 處理文字
def stringprocessing(imgtostr):

    print(imgtostr)
    """
        datetimestr = imgtostr.split("\n")[0]

        try:
            datetimestr = datetime.strptime(datetimestr, '%Y/%m/%d %H:%M:%S')

            print(datetimestr)

        except ValueError:
            pass  # handle invalid date
        else:
            pass  # handle valid date
    """
    datetimestr = imgtostr.split("\n")[0]
    print(datetimestr)
    
    try:
        # datetimestr = datetime.strptime(datetimestr, '%Y/%m/%d %H:%M:%S') # avi
        datetimestr = datetime.strptime(datetimestr, '%Y-%m-%d %H:%M:%S') # mp4
        datetimestr = datetimestr.strftime('%Y-%m-%d %H:%M:%S')
        # print(datetimestr)
        return datetimestr
    
    except ValueError:
        print("值錯誤")
        pass  # handle invalid date
    else:
        print("其他錯誤")
        pass  # handle valid date
    



# 寫文件
def writelog(strlist):

    #txt path
    txtPath = r"./timestr.txt"
    ## 先確認該檔是否存在
    # 沒有就建立

    if os.path.isfile(txtPath):
        
        print("File exist")

        starttime = datetime.fromtimestamp(strlist[0])
        print(starttime)

        # 寫檔    
        with open(txtPath, 'a') as f:
            
            #開始時間,結束時間
            # rstr = strlist[0] +","+ strlist [1]+ "," + strlist[2]
            rstr = f"{strlist[0]}, {strlist [1]}, {strlist[2]}"
            
            f.write(f"{rstr}\n")

            return "ok"

    else:
        print("not")

    
# 讀檔
def vidodfile(filepath):


    return

# timestamp to datetime
def converttimestamp():
    # 取出檔名上的時間 做轉換
    timestamp = (1647475937226) / 1000        
    # dt_obj = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') # 2022-03-17 08:12:17
    dt_obj = datetime.fromtimestamp(timestamp)
    print(filename)


if __name__ == "__main__":

    
    """影片檔案"""
    # filePath = r"./testervideo/001.mp4" area > 3500
    filePath = r"./testervideo/002.avi" # area > 100
    # filePath = r"D:\\testervideo\\001.mp4"
    # filePath = r"D:\\testervideo\\002.avi"
    # filePath = "D:\\testervideo\\003.3gp"

    if os.path.exists(filePath):
        
        # 取資料夾名稱
        dirname = os.path.dirname(filePath).split("/")[-1]

        # 取檔名
        # filename = os.path.basename(filePath)

        objectdetection(filePath)
        
        # 影片總長度
        videolenstr =  videolen(filePath) 
    else:
        print(f"檔案不存在!!")  

    # mystr = 

    # 影片長度
    # lenstr =  videolen(filePath)
    #　print(lenstr)



