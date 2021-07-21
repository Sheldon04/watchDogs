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
        self.conf = {'save_path': './img/', 'min_motion_frames': 10, 'enable_save_img': False}
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
        # fgmask = cv2.dilate(fgmask, None, iterations=2)
        return fgmask

    def stop_video(self):
        if not self.video_writer is None:
            self.video_writer.release()
            self.video_writer = None

    def start_video(self, size):
        if self.video_writer is None:
            self.video_writer = cv2.VideoWriter(self.conf['save_path']
                                                + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.avi',
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
        motion_cnt = 0
        static_cnt = 0
        pre_motion_num = 0
        pre_frame = None
        while True:
            start = time.time()
            grabbed, frame_lwpCV = self.camera.read()  # 读取视频流
            # new_frame = frame_lwpCV.copy()
            gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)  # 转灰度图
            gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (21, 21), 0)
            gray_lwpCV = cv2.resize(gray_lwpCV, size)
            # frame_lwpCV = cv2.resize(frame_lwpCV, (500, 500))
            if pre_frame is None:
                pre_frame = gray_lwpCV

            if not grabbed:
                break
            end = time.time()

            # 运动检测部分
            seconds = end - start
            if seconds < 1.0 / fps:
                time.sleep(1.0 / fps - seconds)
            fgmask = cv2.resize(self.get_fgmask(frame_lwpCV), size)
            # 在完成对帧的灰度转换和平滑后，就可计算与背景帧的差异，并得到一个差分图（different map）
            # 还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，从而对孔（hole）和缺陷（imperfection）进行归一化处理
            # 背景移除
            abs_mask = cv2.absdiff(gray_lwpCV, pre_frame)
            fgthred = cv2.threshold(fgmask, 10, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.threshold(abs_mask, 10, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=1)
            new_abs = cv2.absdiff(thresh, fgthred)
            contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) - pre_motion_num > 20:
                # TODO 按照物体移动速度
                pass
            for c in contours:
                if cv2.contourArea(c) < 500 or cv2.contourArea(c) > 50000:
                    static_cnt += 1
                    if static_cnt > 10:
                        self.stop_video()
                        static_cnt = 0
                        motion_cnt = 0
                    continue

                motion_cnt += 1
                # 有移动物体
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(fgmask, (x, y), (x + w, y + h), (255, 255, 0), 2)
                cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 255, 255), 2)
                # cv2.imshow('fgmask', fgmask)
                # cv2.imshow('lwpCVWindow', frame_lwpCV)

                # if not flag:
                #     tracker = cv2.TrackerKCF_create()
                #     bbox = cv2.selectROI(frame_lwpCV, False)
                #     # print(bbox)
                #     # bbox = (x, y, w, h)
                #     print(bbox)
                #     ok = tracker.init(frame_lwpCV, bbox)
                #     flag = True
                #
                # ok, bbox = tracker.update(frame_lwpCV)
                # # if ok:
                # # new_frame = frame_lwpCV.copy()
                # p1 = (int(bbox[0]), int(bbox[1]))
                # p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                # cv2.rectangle(new_frame, p1, p2, (255, 0, 0), 2, 1)

                # Images
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

                if motion_cnt > self.conf['min_motion_frames'] and self.conf['enable_save_img']:
                    self.start_video(size)
                    self.video_writer.write(frame_lwpCV)
                    # TODO 测试后删除
                    if motion_cnt > 1000:
                        self.video_writer.release()
                        print('stop')

            yield frame_lwpCV, fgmask, thresh, new_abs

            pre_motion_num = motion_cnt
            pre_frame = gray_lwpCV

            if cv2.waitKey(25) & 0xFF == ord('q'):
                self.camera.release()
                cv2.destroyAllWindows()
                break
        # When everything done, release the capture
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    d = Detector(1)
    for test, mask, abs, new in d.run():
        cv2.imshow('test', test)
        cv2.imshow('mask', mask)
        cv2.imshow('abs', abs)
        cv2.imshow('rel_abs', new)
        # cv2.imshow('new', new)

