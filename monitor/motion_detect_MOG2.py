import cv2
import time
import math
import torch
from datetime import datetime
import numpy as np

# Model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5x, custom

# pathf = 'C:\\Users\\ASUS\\Desktop\\data\\haarcascade_frontalface_default.xml'
# pathe = 'C:\\Users\\ASUS\\Desktop\\data\\haarcascade_eye.xml'

# save_path = './face/'
# face_cascade = cv2.CascadeClassifier(pathf)
# eye_cascade = cv2.CascadeClassifier(pathe)
class Detector:
    def __init__(self, choice):
        self.conf = {'save_path': './img/', 'min_motion_frames': 10, 'enable_save_img': True}
        self.video_writer = None
        if choice == 0:
            # video="http://admin:admin@192.168.43.1:8081"   #此处@后的ipv4 地址需要改为app提供的地址
            video = "http://admin:123456@100.58.198.227:8081"
            self.camera = cv2.VideoCapture(video)
            self.camera.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        else:
            file_path = 'C:\\Users\\ASUS\\Desktop\\data\\example video.avi'
            self.camera = cv2.VideoCapture(file_path)

        # 判断视频是否打开
        if self.camera.isOpened():
            print('Open')
        else:
            print('摄像头未打开')


    def run(self):
        # 测试用,查看视频size
        size = (int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print('size:' + repr(size))

        fps = 30  # 帧率
        fgbg = cv2.createBackgroundSubtractorMOG2()
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        cnt = 0
        while True:
            start = time.time()
            grabbed, frame_lwpCV = self.camera.read()  # 读取视频流
            # frame_lwpCV = cv2.resize(frame_lwpCV, (500, 500))

            fgmask = fgbg.apply(frame_lwpCV)
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

            if not grabbed:
                break
            end = time.time()

            # 运动检测部分
            seconds = end - start
            if seconds < 1.0 / fps:
                time.sleep(1.0 / fps - seconds)
            fgmask = cv2.resize(fgmask, size)
            fgmask = cv2.GaussianBlur(fgmask, (21, 21), 0)
            fgmask = cv2.dilate(fgmask, None, iterations=10)
            # 在完成对帧的灰度转换和平滑后，就可计算与背景帧的差异，并得到一个差分图（different map）
            # 还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，从而对孔（hole）和缺陷（imperfection）进行归一化处理
            # 背景移除
            thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]
            contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for c in contours:
                cnt += 1
                if cv2.contourArea(c) < 1500:
                    if not self.video_writer is None:
                        self.video_writer.release()
                        self.video_writer = None
                    continue
                # 有移动物体
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(fgmask, (x, y), (x + w, y + h), (255, 255, 0), 2)
                cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (255, 255, 0), 2)
                # cv2.imshow('fgmask', fgmask)
                # cv2.imshow('lwpCVWindow', frame_lwpCV)
                if cnt > self.conf['min_motion_frames'] and self.conf['enable_save_img']:
                    if self.video_writer is None:
                        self.video_writer = cv2.VideoWriter(self.conf['save_path'],
                                                            cv2.VideoWriter_fourcc(*'AVC1'), 20.0, size, True)
                    self.video_writer.write(frame_lwpCV)

                yield frame_lwpCV
                # cv2.imshow(c)
                # # yolov5检测物体
            # # Images
            # img = frame_lwpCV  # or file, PIL, OpenCV, numpy, multiple
            # # Inference
            # results = model(img)
            # # Results
            # # results.show()  # or .show(), .save(), .crop(), .pandas(), etc.
            # # print(type(results.pandas().xyxy[0]['xmin'].values[0]))
            # if len(results.pandas().xyxy[0]['xmin'].values) != 0:
            #     cv2.rectangle(frame_lwpCV, (
            #         int(results.pandas().xyxy[0]['xmin'].values[0]), int(results.pandas().xyxy[0]['ymin'].values[0])),
            #         (int(results.pandas().xyxy[0]['xmax'].values[0]), int(results.pandas().xyxy[0]['ymax'].values[0])),
            #             (255, 255, 0), 2)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                self.camera.release()
                cv2.destroyAllWindows()
                break
        # When everything done, release the capture
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    d = Detector(1)
    for test in d.run():
        cv2.imshow('test', test)
