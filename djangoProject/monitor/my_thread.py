import os
import threading
import time

import cv2
import face_recognition
from django.contrib.auth.models import User
from django.core.mail import send_mail

from datamodel.models import invationRecord
import djangoProject.settings as settings


class Invasion_Record_Saver(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, _date, _time, invasion_num, level=1, camera_id=1, area='仓库'):
        threading.Thread.__init__(self)
        self._date = _date
        self._time = _time
        self.invasion_num = invasion_num
        self.level = level
        self.camera_id = camera_id
        self.area = area

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        # print('date ', self._date, ' time ', self._time, ' num ', self.invasion_num)
        try:
            invationRecord.objects.create(date=self._date, time=self._time, invation_num=self.invasion_num,
                                          level=1, camera_id=1, area='厨房')
        except Exception as e:
            print(e)
            print('保存入侵信息失败')


# class Yolo_Thread(threading.Thread):  # 继承父类threading.Thread
#     def __init__(self, d):
#         threading.Thread.__init__(self)
#         # self.detector = d
#
#     def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
#         # self.detector.run2()
#         d = Detector()
#         d.run2()

class Email_Sender(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, known_face_encodings, _date, _time, invasion_num, level=1, camera_id=1, area='仓库', ):
        threading.Thread.__init__(self)
        self._date = _date
        self._time = _time
        self.invasion_num = invasion_num
        self.level = level
        self.camera_id = camera_id
        self.area = area
        self.known_face_encodings = known_face_encodings

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        self.process_pic()

    def process_pic(self):
        # Grab a single frame of video
        times = self._time.split(':')
        filename = self._date + '-' + times[0] + '-' + times[1] + '-' + times[2]
        path = 'E:\\watchDogs\\djangoProject\\monitor\\video\\' + filename
        print('path ', path)
        file_num = sum([os.path.isfile(path + '/' + listx) for listx in os.listdir(path)])
        print('pic num ', file_num)
        for i in range(1, file_num + 1):
            frame = cv2.imread(path + '\\' + str(i) + '.jpg')
            print('processing ' + str(i) + '.jpg')
            scale = 0.5
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=1,
                                                             model="cnn")
            print('face locate done')
            face_encodings = face_recognition.face_encodings(rgb_small_frame, known_face_locations=face_locations,
                                                             num_jitters=20)
            print('face encoded done')
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.5)
                print('compare done')
                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    return

        self.send_my_mail()

    def send_my_mail(self):
        emails = list(User.objects.filter(is_superuser=1).values('email'))
        email_list = []
        for email in emails:
            email_list.append(email['email'])
        title = "美团骑手offer"
        msg = "您的{}遭到入侵！\n入侵数量：{}\n警戒等级：{}\n报警来自摄像头{}\n日期：{}\n时间：{}" \
            .format(self.area, self.invasion_num, self.level, self.camera_id, self._date, self._time)
        email_from = settings.DEFAULT_FROM_EMAIL
        reciever = email_list
        # 发送邮件
        try:
            send_mail(title, msg, email_from, reciever)
            print('send mail')
        except Exception as e:
            print(e)
            print('邮件发送失败')
