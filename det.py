import cv2
import numpy as np
import os

videoPath = r"D:\\testervideo\\001.mp4"

outputPath = r"D:\\pythonfile\\opencv\\outputimg\\"

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


# 開啟影片檔
cap = cv2.VideoCapture(videoPath)

# 取得畫面尺寸
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# 計算畫面面積
area = width * height

# 初始化平均畫面
ret, frame = cap.read()
avg = cv2.blur(frame, (4, 4))
avg_float = np.float32(avg)


out = cv2.VideoWriter(
    'output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (640,480))

# 輸出圖檔用的計數器
outputCounter = 0


while(cap.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == False:
        break
    

    # 模糊處理
    blur = cv2.blur(frame, (4, 4))

    # 計算目前影格與平均影像的差異值
    diff = cv2.absdiff(avg, blur)

    # 將圖片轉為灰階
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)


    # 篩選出變動程度大於門檻值的區域
    ret, thresh = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)    
    

    # 使用型態轉換函數去除雜訊
    kernel = np.ones((7, 7), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # 產生等高線
    contours, hierarchy  = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    

    hasMotion = False

    for c in contours:
        # 忽略太小的區域
        if cv2.contourArea(c) < 2500:
            continue

        hasMotion = True

        # 計算等高線的外框範圍
        x, y, w, h = cv2.boundingRect(c)

        # 畫出外框
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        
        #if hasMotion:
            # 儲存有變動的影像
        #    cv2.imwrite(f"{outputPath}{outputCounter}.jpg", frame)
        #    outputCounter += 1
        
        



    cv2.imshow('gray', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): # 按Q
        break

    # 更新平均影像
    cv2.accumulateWeighted(blur, avg_float, 0.01)
    avg = cv2.convertScaleAbs(avg_float)

cap.release()

