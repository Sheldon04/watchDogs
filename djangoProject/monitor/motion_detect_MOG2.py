import base64

import cv2
import time
from datetime import datetime
import os
import torch

# 使用MOG2模型进行移动物体标注更稳定，但是易出现噪点（如当场景中大量移动物体移出场景时）
# 使用固定背景进行背景减除在上述场景下不会出现噪点，但是需要定期更新背景图
from monitor.my_thread import Email_Sender


class Detector:
    def __init__(self, choice, model=None, known_face_encodings=None):
        self.conf = {'save_path': './video/', 'min_motion_frames': 10, 'enable_save_img': True}
        self.video_writer = None
        # 使用ip摄像头
        if choice == 0:
            # video="http://admin:admin@192.168.43.1:8081"   #此处@后的ipv4 地址需要改为app提供的地址
            video = "http://admin:123456@100.58.198.227:8081"
            self.camera = cv2.VideoCapture(video)
            self.camera.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        # 使用本地视频文件（测试用）
        elif choice == 1:
            # file_path = 'C:\\Users\\ASUS\\Desktop\\data\\road.kux'
            file_path = 'C:\\Users\\ASUS\\Desktop\\face_recognition\\unknown\\hall2_mid.mp4'
            # file_path = 'C:\\Users\\ASUS\\Desktop\\data\\example video.avi'
            self.camera = cv2.VideoCapture(file_path)
        # 使用rtmp转发服务器读取视频流
        else:
            file_path = 'http://47.106.148.74:80/tv_file/test.m3u8'
            # file_path = 'C:\\Users\\ASUS\\Desktop\\data\\example video.avi'
            self.camera = cv2.VideoCapture(file_path)

        # 场景的静态背景，用于计算差分图（run1()）
        # self.bg = cv2.imread('./monitor/data/back.jpg')
        # self.bg = cv2.cvtColor(self.bg, cv2.COLOR_BGR2GRAY)  # 转灰度图
        # self.bg = cv2.GaussianBlur(self.bg, (21, 21), 0)
        # Model
        # self.yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom
        self.yolo = model  # or yolov5m, yolov5l, yolov5x, custom
        self.known_face_encodings = known_face_encodings

        # 判断视频是否打开
        if self.camera.isOpened():
            print('Open')
        else:
            print('摄像头未打开')

    # 使用MOG2模型进行背景减除
    def get_fgmask(self, frame):
        fgmask = self.fgbg.apply(frame)
        # 进行形态学开运算，即先腐蚀，再膨胀，以去除噪声
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)
        # fgmask = cv2.GaussianBlur(fgmask, (21, 21), 0)
        # 再进行一次膨胀，扩大高亮区域（移动物体）
        fgmask = cv2.dilate(fgmask, None, iterations=2)
        return fgmask

    # 停止记录入侵视频
    def stop_video(self, _date, _time, num):
        if not self.video_writer is None:
            self.video_writer.release()
            self.video_writer = None
            t = Email_Sender(self.known_face_encodings, _date, _time, num)
            t.start()
            print('stop')


    # 开始记录入侵视频
    def start_video(self, size, time):
        if self.video_writer == None:
            print('start')
            os.mkdir('./monitor/video/' + time)
            self.video_writer = cv2.VideoWriter('./monitor/video/'
                                                + time + '.avi',
                                                cv2.VideoWriter_fourcc(*'XVID'), 20.0, size, True)


    # 使用MOG2模型进行背景减除
    def run(self):
        flag = False
        # 测试用,查看视频size
        size = (int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        # print('size:' + repr(size))

        fps = 30  # 帧率
        # self.fgbg = cv2.createBackgroundSubtractorMOG2()
        # self.fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
        self.fgbg = cv2.createBackgroundSubtractorKNN(detectShadows=True)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        motion_body_cnt = 0     # 一帧中的移动物体
        motion_frame_cnt = 0    # 出现移动物体的帧数，当帧数大于一定值后，认为有入侵发生
        pre_motion_num = 0      # 暂时没用
        is_first_invade = True  # 一次入侵中，是否第一次被记录，用于判断入侵开始时间
        is_invade = False       # 是否有入侵
        invasion_date = None
        invasion_time = None
        while True:
            start = time.time()
            grabbed, frame_lwpCV = self.camera.read()  # 读取视频流
            motion_body_cnt = 0
            if not grabbed:
                break

            invade_time = None
            return_flag = False

            # 背景减除后的图像
            fgmask = cv2.resize(self.get_fgmask(frame_lwpCV), size)
            fgmask = cv2.erode(fgmask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
            fgmask = cv2.dilate(fgmask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 3)), iterations=2)
            thresh = cv2.threshold(fgmask, 244, 255, cv2.THRESH_BINARY)[1]
            # 查找图像中的高亮区域的轮廓
            contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            is_motion = False
            for c in contours:
                # 删除过小或过大的区域
                if cv2.contourArea(c) < 1500 or cv2.contourArea(c) > 90000:
                    continue
                # 入侵发生
                motion_body_cnt += 1
                is_motion = True
                # 有移动物体
                (x, y, w, h) = cv2.boundingRect(c)
                # 标记
                cv2.rectangle(fgmask, (x, y), (x + w, y + h), (255, 255, 0), 2)
                cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 255, 255), 2)

                # 开始记录入侵视频
                if motion_frame_cnt > self.conf['min_motion_frames'] and self.conf['enable_save_img'] and is_first_invade:
                    is_invade = True
                    now = datetime.now()
                    self.filename = now.strftime("%Y-%m-%d-%H-%M-%S")
                    invasion_date = now.strftime("%Y-%m-%d")
                    invasion_time = now.strftime("%H:%M:%S")
                    self.start_video(size, self.filename)
                    # # TODO 测试后删除
                    # if motion_body_cnt > 500:
                    #     self.conf['enable_save_img'] = False
                    #     self.video_writer.release()
                    #     print('stop')

            # 没有移动物体时停止录制视频
            if not is_motion:
                # print('invade stop')
                self.stop_video(None, None, None)
                is_first_invade = True
                is_invade = False
                motion_frame_cnt = 0
            else:
                motion_frame_cnt += 1
                if is_invade and is_first_invade:
                    print('invade start')
                    is_first_invade = False
                    return_flag = True

            if self.video_writer != None:
                self.video_writer.write(frame_lwpCV)
                # if motion_frame_cnt % 90 == 0:
                #     print('save')
                #     path = './video/' + self.filename + '/' + str(motion_frame_cnt / 90) + '.jpg'
                #     print(path)
                #     cv2.imwrite(path, frame_lwpCV)

            # 返回移动物体标注后的图像，移动物体数，是否为首次入侵，入侵时间
            yield frame_lwpCV, False, motion_body_cnt, invasion_date, invasion_time
            cv2.imshow('thresh', thresh)
            cv2.imshow('mask', fgmask)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.camera.release()
                cv2.destroyAllWindows()
                break
        # When everything done, release the capture
        self.camera.release()
        cv2.destroyAllWindows()

    # 使用固定背景的背景减除
    def run1(self):
        flag = False
        # 测试用,查看视频size
        size = (int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        fps = 30  # 帧率
        motion_body_cnt = 0  # 一帧中的移动物体
        motion_frame_cnt = 0  # 出现移动物体的帧数
        pre_motion_num = 0
        is_first_invade = True
        is_invade = False
        while True:
            start = time.time()
            grabbed, frame_lwpCV = self.camera.read()  # 读取视频流
            gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)  # 转灰度图
            gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (21, 21), 0)

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

            # 背景移除
            # 在完成对帧的灰度转换和平滑后，就可计算与背景帧的差异，并得到一个差分图（different map）
            # 还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，从而对孔（hole）和缺陷（imperfection）进行归一化处理
            img_delta = cv2.absdiff(gray_lwpCV, self.bg)
            thresh = cv2.threshold(img_delta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=4)
            contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 之后的和前面差不多
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
                cv2.rectangle(thresh, (x, y), (x + w, y + h), (255, 255, 0), 2)
                cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 100, 255), 2)

                if motion_frame_cnt > self.conf['min_motion_frames'] and self.conf['enable_save_img'] and is_first_invade:
                    is_invade = True
                    invade_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                    self.start_video(size, invade_time)
                    self.video_writer.write(frame_lwpCV)
                    # TODO 测试后删除
                    if motion_body_cnt > 500:
                        self.conf['enable_save_img'] = False
                        self.video_writer.release()
                        print('stop')

            # 没有移动物体时停止录制视频
            if not is_motion:
                # print('invade stop')
                self.stop_video()
                is_first_invade = True
                is_invade = False
                motion_frame_cnt = 0
            else:
                motion_frame_cnt += 1
                if is_invade and is_first_invade:
                    print('invade start')
                    is_first_invade = False
                    return_flag = True

            yield frame_lwpCV, motion_body_cnt, return_flag, invade_time

            pre_motion_num = motion_body_cnt
            # pre_frame = gray_lwpCV

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.camera.release()
                cv2.destroyAllWindows()
                break
        # When everything done, release the capture
        self.camera.release()
        cv2.destroyAllWindows()

    def run2(self):
        # 测试用,查看视频size
        size = (1280, 720)

        person_cnt = 0  # 一帧中的移动物体
        is_first_invade = True  # 一次入侵中，是否第一次被记录，用于判断入侵开始时间
        is_invade = False  # 是否有入侵
        invade_frame_cnt = 0
        invasion_date = None
        invasion_time = None
        while True:
            return_flag = False

            grabbed, frame_lwpCV = self.camera.read()  # 读取视频流
            frame_lwpCV = cv2.resize(frame_lwpCV, size)

            # yolov5
            video = frame_lwpCV.copy()
            # video = frame_lwpCV[:, :, ::-1]
            # Inference
            results = self.yolo(video)

            if invade_frame_cnt > self.conf['min_motion_frames'] and self.conf['enable_save_img'] and is_first_invade:
                is_invade = True
                now = datetime.now()
                self.filename = now.strftime("%Y-%m-%d-%H-%M-%S")
                invasion_date = now.strftime("%Y-%m-%d")
                invasion_time = now.strftime("%H:%M:%S")
                self.start_video(size, self.filename)
            # if 'person' in results.pandas().xyxy[0]:
            #     print('True')
            # 有入侵
            if 0 in list(results.pandas().xyxy[0]['class']):
                invade_frame_cnt += 1
                if invade_frame_cnt > 500:
                    # self.conf['enable_save_img'] = False
                    # self.video_writer.release()
                    self.stop_video(invasion_date, invasion_time, person_cnt)
                    is_first_invade = True
                    is_invade = False
                    invade_frame_cnt = 0
                    print('forced stop')
                    # self.conf['enable_save_img'] = False
                if is_invade and is_first_invade:
                    print('invade start')
                    is_first_invade = False
                    return_flag = True
                    person_cnt = list(results.pandas().xyxy[0]['class']).count(0)
            else:
                # 没有移动物体时停止录制视频
                # print('invade stop')
                self.stop_video(invasion_date, invasion_time, person_cnt)
                is_first_invade = True
                is_invade = False
                invade_frame_cnt = 0

            results.render()  # updates results.imgs with boxes and labels

            if self.video_writer != None:
                self.video_writer.write(results.imgs[0])
                if invade_frame_cnt % 90 == 0:
                    print('save')
                    path = './monitor/video/' + self.filename + '/' + str(int(invade_frame_cnt / 90)) + '.jpg'
                    print(path)
                    cv2.imwrite(path, frame_lwpCV)

            # cv2.imshow('yolo', results.imgs[0])

            # 返回移动物体标注后的图像，移动物体数，是否为首次入侵，入侵时间
            yield results.imgs[0], return_flag, person_cnt, invasion_date, invasion_time

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # When everything done, release the capture
        self.camera.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    d = Detector(1)
    for test, mask, is_invade, invade_time, _ in d.run():
        cv2.imshow('test', test)
        retval, buffer = cv2.imencode('.jpg', test)
        pic_str = base64.b64encode(buffer)
