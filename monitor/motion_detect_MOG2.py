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
            file_path = 'C:\\Users\\ASUS\\Desktop\\data\\road.kux'
            # file_path = 'C:\\Users\\ASUS\\Desktop\\data\\example video.avi'
            self.camera = cv2.VideoCapture(file_path)

        # 判断视频是否打开
        if self.camera.isOpened():
            print('Open')
        else:
            print('摄像头未打开')

    def get_fgmask(self, frame):
        fgmask = self.fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)
        # fgmask = cv2.GaussianBlur(fgmask, (21, 21), 0)
        fgmask = cv2.dilate(fgmask, None, iterations=2)
        return fgmask

    def stop_video(self):
        if not self.video_writer is None:
            self.video_writer.release()
            self.video_writer = None

    def start_video(self, size, time):
        if self.video_writer == None:
            print('start')
            self.video_writer = cv2.VideoWriter(self.conf['save_path']
                                                + time + '.avi',
                                                cv2.VideoWriter_fourcc(*'XVID'), 20.0, size, True)

    def run(self):
        flag = False
        # 测试用,查看视频size
        size = (int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print('size:' + repr(size))

        fps = 30  # 帧率
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        # self.fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        motion_body_cnt = 0      # 一帧中的移动物体
        motion_frame_cnt = 0    # 出现移动物体的帧数
        pre_motion_num = 0
        is_first_invade = True
        is_invade = False
        while True:
            start = time.time()
            grabbed, frame_lwpCV = self.camera.read()  # 读取视频流
            motion_body_cnt = 0
            if not grabbed:
                break
            end = time.time()
            invade_time = None
            return_flag = False
            # 运动检测部分
            seconds = end - start
            if seconds < 1.0 / fps:
                time.sleep(1.0 / fps - seconds)
            fgmask = cv2.resize(self.get_fgmask(frame_lwpCV), size)
            # 在完成对帧的灰度转换和平滑后，就可计算与背景帧的差异，并得到一个差分图（different map）
            # 还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，从而对孔（hole）和缺陷（imperfection）进行归一化处理
            # 背景移除
            contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) - pre_motion_num > 20:
                # TODO 按照物体移动速度
                pass
            is_motion = False
            for c in contours:
                if cv2.contourArea(c) < 500 or cv2.contourArea(c) > 50000:
                    continue
                motion_body_cnt += 1
                is_motion = True
                # 有移动物体
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(fgmask, (x, y), (x + w, y + h), (255, 255, 0), 2)
                cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 255, 255), 2)

                if motion_frame_cnt > self.conf['min_motion_frames'] and self.conf['enable_save_img']:
                    is_invade = True
                    invade_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                    self.start_video(size, invade_time)
                    self.video_writer.write(frame_lwpCV)
                    # TODO 测试后删除
                    if motion_body_cnt > 500:
                        self.conf['enable_save_img'] = False
                        self.video_writer.release()
                        print('stop')

            if not is_motion:
                # print('invade stop')
                self.stop_video()
                is_first_invade = True
            else:
                motion_frame_cnt += 1
                if is_invade and is_first_invade:
                    print('invade start')
                    is_first_invade = False
                    is_invade = False
                    return_flag = True

            yield frame_lwpCV, motion_body_cnt, return_flag, invade_time

            pre_motion_num = motion_body_cnt
            # pre_frame = gray_lwpCV

            if cv2.waitKey(25) & 0xFF == ord('q'):
                self.camera.release()
                cv2.destroyAllWindows()
                break
        # When everything done, release the capture
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    d = Detector(1)
    for test, mask, is_invade, invade_time in d.run():
        cv2.imshow('test', test)
        cv2.imshow('mask', mask)
        if is_invade:
            print(invade_time)
