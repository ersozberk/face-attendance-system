import os.path
import datetime
import pickle

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
from test import test
import util

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title('METAYILDIZ BİLİŞİM ÇALIŞAN TAKİP SİSTEMİ')
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = util.get_button(self.main_window, 'GİRİŞ', 'green', self.login)
        self.login_button_main_window.place(x=750, y=200)

        self.logout_button_main_window = util.get_button(self.main_window, 'ÇIKIŞ', 'red', self.logout)
        self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'YENİ KULLANICI KAYDET', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_RGB2BGR)
        # Detect the faces
        faces = face_cascade.detectMultiScale(img_, 1.3, 5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img_, (x, y), (x + w, y + h), (10, 159, 255), 2)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):

        label = test(
                image=self.most_recent_capture_arr,
                model_dir='/Users/berkersoz/Desktop/face-attendance-system-master/Silent-Face-Anti-Spoofing/resources/anti_spoof_models',
                device_id=0
                )

        if label == 1:

            name = util.recognize(self.most_recent_capture_arr, self.db_dir)

            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box('Ups...', 'Bilinmeyen kullanıcı. Lütfen kayıt yapın ve tekrar deneyin.')
            else:
                util.msg_box('Tekrar Hoşgeldin !', 'Hoşgeldiniz, {}.'.format(name))
                with open(self.log_path, 'a') as f:
                    f.write('{},{},GİRİŞ\n'.format(name, datetime.datetime.now()))
                    f.close()

        else:
            util.msg_box('Hey, bu foto gerçek değil!', 'Sen sahtesin!')

    def logout(self):

        label = test(
                image=self.most_recent_capture_arr,
                model_dir='/Users/berkersoz/Desktop/face-attendance-system-master/Silent-Face-Anti-Spoofing/resources/anti_spoof_models',
                device_id=0
                )

        if label == 1:

            name = util.recognize(self.most_recent_capture_arr, self.db_dir)

            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box('Ups...', 'Bilinmeyen kullanıcı. Lütfen kayıt yapın ve tekrar deneyin.')
            else:
                util.msg_box('Sağlıklı Günler !', 'Hoşçakal, {}.'.format(name))
                with open(self.log_path, 'a') as f:
                    f.write('{},{},ÇIKIŞ\n'.format(name, datetime.datetime.now()))
                    f.close()

        else:
            util.msg_box('Hey, bu foto gerçek değil!', 'Sen sahtesin!')


    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'KABUL EDİLDİ', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'YENİDEN DENEYİN', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'LÜTFEN, \nİSMİ GİRİNİZ:')
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]

        file = open(os.path.join(self.db_dir, '{}.pickle'.format(name)), 'wb')
        pickle.dump(embeddings, file)

        util.msg_box('BAŞARILI!', 'Kullanıcı başarıyla kaydedildi!')

        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()
