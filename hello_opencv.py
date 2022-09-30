import cv2
import numpy as np
import os


# 影片檔案
#videoFile = "D:\\img\\1647475937226-41-0.3gp"
# videoFile = "D:\img\1FAT_29\2021_12\1647409822548-41-0.avi"
videoPath = "D:\\testervideo\\001.mp4"
# videoPath = "D:\\testervideo\\002.avi"
# videoPath = "D:\\testervideo\\003.3gp"


# 輸出目錄
# outputFolder = "D:\\my_output\\1FAT_29\\1204\\1\\"
#outputFolder = "D:\\my_output\\"
#outputPath = "D:\\pythonfile\\opencv\\outputimg\\"

# 自動建立目錄
#if not os.path.exists(outputFolder):
#  os.makedirs(outputFolder)

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

# 輸出圖檔用的計數器
outputCounter = 0

while(cap.isOpened()):
  # 讀取一幅影格
  ret, frame = cap.read()

  # 若讀取至影片結尾，則跳出
  if ret == False:
    break

  # 模糊處理
  blur = cv2.blur(frame, (4, 4))

  # 計算目前影格與平均影像的差異值
  diff = cv2.absdiff(avg, blur)

  # 將圖片轉為灰階
  gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

  # 篩選出變動程度大於門檻值的區域
  ret, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)

  # 使用型態轉換函數去除雜訊
  kernel = np.ones((5, 5), np.uint8)
  thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
  thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

  # 產生等高線
  contours, hierarchy  = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  hasMotion = False

  for c in contours:
    # 忽略太小的區域
    if cv2.contourArea(c) < 2500:
      continue


    hasMotion = True

    # 計算等高線的外框範圍
    (x, y, w, h) = cv2.boundingRect(c)

    # 畫出外框
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

  
    #if hasMotion:
        # 儲存有變動的影像
        # cv2.imwrite("%s/output_%04d.jpg" % (outputPath, outputCounter), frame)
    #outputCounter += 1
    
    

  

  # 更新平均影像
  cv2.accumulateWeighted(blur, avg_float, 0.01)
  avg = cv2.convertScaleAbs(avg_float)

  
  cv2.imshow('日期時間', frame)    

  if cv2.waitKey(1) & 0xFF == ord('q'): # 按Q                

      break




cap.release()