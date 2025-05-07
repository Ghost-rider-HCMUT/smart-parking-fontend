import re
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import cv2
from time import sleep
import numpy as np
import array as arr
import math
import sys
import requests
import serial
import os
from imutils.video import VideoStream
from imutils import face_utils
from PIL import Image
import imutils
import pytesseract
import pygame
pygame.mixer.init()

from ultralytics import YOLO  # Import YOLO from the ultralytics library
from paddleocr import PaddleOCR
import time
from datetime import datetime
#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#ser = serial.Serial('/dev/ttyUSB0',9600)

class Page1Test(QMainWindow):
    def __init__(self):
        super().__init__()
        # Khởi tạo UI
        uic.loadUi("admin/page1.ui", self)
        self.cardId = ""
        # Khởi tạo các biến
        self.mode = 0
        self.dk_vao = 0
        self.dk_ra = 0
        self.con_lai = 0
        self.kq = 0
        self.cp = 0
        self.mode_ht = 0
        self.tt_vao = 0
        self.tt_ra = 0
        self.vr = 0
        self.dc_ra = 0
        self.time2 = 0
        self.time_vao = 0
        self.time_ra = 0
        self.tien = 0
        self.tgian_vao = ""
        self.tgian_ra = ""
        self.img = None
        self.data = '' 
        self.vr = 0
        self.tong_xe = self.get_available_parking_lot()["countAll"]
        print("tong xe = ",self.tong_xe)
        self.con_lai = self.get_available_parking_lot()["countAvailable"]
        print("con lai = ",self.con_lai)
        self.so_xe = self.tong_xe - self.con_lai

        # Khởi tạo Serial
        self.ser = serial.Serial('COM3', baudrate=9600, timeout=1)
        print(self.ser.name)

        # Khởi tạo Camera
        self.vs = VideoStream(src=0).start() #cam vào
        self.vs2 = VideoStream(src=1).start() #cam ra

        # Khởi tạo YOLO và OCR
        self.license_plate_detector = YOLO(r"number-plate-recognition-using-yolov11\models\license_plate_detector.pt")
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')

        # Kết nối các nút
        self.BT_AUTO.clicked.connect(self.auto)
        self.BT_MAN.clicked.connect(self.manual)
        self.BT_VAO.clicked.connect(self.vao)
        self.BT_RA.clicked.connect(self.ra)

        # Khởi tạo Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.Time)
        self.timer.start(50)

    def Time(self):
        #-------------------thời gian-------------------
        today = datetime.today()
        day = today.strftime("%d/%m/%Y")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time_present = current_time + " - " + day
        self.lb_tgian.setText(time_present)
        
        #-----------------nhận dữ liệu------------------
        if(self.ser.in_waiting > 0):
            try:
                s = self.ser.readline()
                try:
                    dataa = s.decode('utf-8').rstrip()
                except UnicodeDecodeError:
                    try:
                        dataa = s.decode('ascii').rstrip()
                    except UnicodeDecodeError:
                        dataa = s.decode('latin-1').rstrip()
                        
                if dataa.startswith("RFID"):
                    index = dataa.find('=')
                    if index != -1:
                        print(f"Parsed Data RFID UID: {dataa}")  
                        self.cardId = dataa[index + 1:].strip()
                
                if dataa.startswith("STATUS"):
                    print(f"Parsed Data status: {dataa}")  
                
                if dataa and '|' in dataa:
                    mang = dataa.split("|")
                    # print(f"Parsed Data: {mang}") 
                    if len(mang) == 7:
                        self.mode_ht = int(mang[0])
                        self.tt_vao = int(mang[1])
                        self.tt_ra = int(mang[2])
                        self.cp = int(mang[3])
                        self.vr = int(mang[4])
                        self.dc_ra = int(mang[5])
            except Exception as e:
                print(f"Lỗi đọc Serial: {e}")
                pass
        self.lb_so_xe.setText(str(self.so_xe))
        self.lb_con_lai.setText(str(self.con_lai))
        
        if self.mode_ht == 0:
            self.lb_mode.setStyleSheet("background-color: rgb(0, 85, 255)")
        if self.mode_ht == 1:
            self.lb_mode.setStyleSheet("background-color: rgb(255, 170, 0)") 
        if self.tt_vao == 0:
            #str_vao = "VÀO: ĐANG ĐÓNG"
            #call.BT_VAO.setText(str_vao)
            self.BT_VAO.setStyleSheet("background-color: rgb(255, 0, 0)") 
        else:
            #str_vao = "VÀO: ĐANG MỞ"
            #call.BT_VAO.setText(str_vao)
            self.BT_VAO.setStyleSheet("background-color: rgb(0, 255, 0)") 
        if self.tt_ra == 0:
            #str_ra = "RA: ĐANG ĐÓNG"
            #call.BT_RA.setText(str_ra)
            self.BT_RA.setStyleSheet("background-color: rgb(255, 0, 0)") 
        else:
            #str_ra = "RA: ĐANG MỞ"
            #call.BT_RA.setText(str_ra)
            self.BT_RA.setStyleSheet("background-color: rgb(0, 255, 0)") 
        if self.so_xe < self.tong_xe:
            '''
            call.lb_so_xe.setStyleSheet("background-color: rgb(85, 255, 0)")
            call.lb_con_lai.setStyleSheet("background-color: rgb(85, 255, 0)")
            '''
            self.lb_tb.setText("CÒN CHỖ TRỐNG")
            self.lb_tb.setStyleSheet("background-color: rgb(85, 255, 0)")
        else:
            '''
            call.lb_so_xe.setStyleSheet("background-color: rgb(255, 0, 0)")
            call.lb_con_lai.setStyleSheet("background-color: rgb(255, 0, 0)")
            '''
            self.lb_tb.setText("ĐÃ HẾT CHỖ")
            self.lb_tb.setStyleSheet("background-color: rgb(255, 0, 0)")
        try:
            # Đọc ảnh từ camera
            frame = self.vs.read()
            frame2 = self.vs2.read()
            #frame = cv2.flip(frame,1)
            # chỉnh kích thước ảnh để tăng tốc độ xử lý
            frame = imutils.resize(frame, width=640)
            frame2 = imutils.resize(frame2, width=640)
            # Hien thi len man hinh
            imgg = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
            pix = QPixmap.fromImage(imgg)
            self.lb_vid.setPixmap(pix)

            imgg2 = QImage(frame2, frame2.shape[1], frame2.shape[0], QImage.Format_RGB888).rgbSwapped()
            pix2 = QPixmap.fromImage(imgg2)
            self.lb_vid2.setPixmap(pix2)
            if self.cp == 1:
                if self.vr == 1:
                    user_detail = self.checkCardIdInUser(self.cardId)
                    checkFlag = self.check_card_id_in_user_transient(self.cardId)

                    if self.so_xe < self.tong_xe:
                        self.img = frame
                        self.xulyanh()
                        status = ""
                        if user_detail and user_detail["licensePlateNumber"] == self.data:
                            status = "OK"
                        elif checkFlag:
                            status = "NOT_OK"
                        else:
                            status = "OK"
                        
                        print("Status:", status)
                        self.ser.write(f'd|{status}\r\n'.encode())
                        self.ser.flush()
                        print("Gửi dữ liệu:", status)
                        pix2 = QPixmap('bien.jpg')
                        self.lb_bien.setPixmap(pix2)
                        time1 = time.time()
                        if time1 - self.time2 >= 7:
                            pygame.mixer.music.load("admin\SOUND\WELCOME.MP3")
                            pygame.mixer.music.play()
                            self.time2 = time.time()
                        self.lb_tgian_vao.setText(time_present)

                    else:
                        print("day xe")
                        time1 = time.time()
                        if time1 - self.time2 >= 7:
                            pygame.mixer.music.load("SOUND\FULL.MP3")
                            pygame.mixer.music.play()
                            self.time2 = time.time()
                if self.vr == 2:
                    self.img = frame2
                    self.xulyanh()
                    pix2 = QPixmap('bien.jpg')
                    self.lb_bien2.setPixmap(pix2)
                self.cp = 0
            if self.dc_ra == 1:
                self.time_ra = time.time()
                tgian_gui = round(self.time_ra - self.time_vao)
                tgian_gui = int(tgian_gui)
                if tgian_gui <= 30:
                    self.tien = "5.000 VND"
                elif tgian_gui <= 40:
                    self.tien = "10.000 VND"
                else:
                    self.tien = "15.000 VND"
                self.lb_tgian_gui.setText(str(tgian_gui) + " s")
                self.lb_tien.setText(self.tien)
                time1 = time.time()
                if time1 - self.time2 >= 3:
                    pygame.mixer.music.load("SOUND\BYE.MP3")
                    pygame.mixer.music.play()
                    self.time2 = time.time()
                    self.dc_ra = 0
            if self.dc_ra == 2:
                time1 = time.time()
                if time1 - self.time2 >= 7:
                    pygame.mixer.music.load("SOUND\ERROR.MP3")
                    pygame.mixer.music.play()
                    self.time2 = time.time()
                    self.dc_ra = 0
        except Exception as e:
            print(f"Lỗi: {e}")

    def xulyanh(self):
        
        license_plates = self.license_plate_detector(self.img)

        # Annotate the image with detected license plates and perform OCR on the detected plates
        for plate in license_plates:
            for bbox in plate.boxes:
                x1, y1, x2, y2 = bbox.xyxy[0]  # Get bounding box coordinates

                # Convert to integers
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

                # Draw rectangle around the detected license plate
                cv2.rectangle(self.img, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # Crop the detected license plate region from the image
                plate_image = self.img[y1:y2, x1:x2]

                # Use PaddleOCR to read the text from the cropped license plate image
                result = self.ocr.ocr(plate_image, cls=True)

                # Extract text from the OCR result
                plate_text = ""
                for line in result[0]:
                    plate_text += line[1][0] + " "  # Add detected text in each line

                # Clean the detected text using regex to remove any characters that are not letters or digits
                self.data = re.sub(r'[^A-Za-z0-9]', '', plate_text.strip())

                cv2.putText(self.img, self.data, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                print("Detected License Plate:", self.data)
        # Save the annotated image with detected text
        cv2.imwrite("bien.jpg", self.img)

        # Update the GUI labels
        if self.vr == 1:
            self.lb_bien_vao.setText(self.data)
        if self.vr == 2:
            self.lb_bien_ra.setText(self.data)

        

    def auto(self):
        self.ser.write(b'a|0\r\n')
        self.ser.flush()

    def manual(self):
        self.ser.write(b'a|1\r\n')
        self.ser.flush()

    def vao(self):
        self.dk_vao = (self.dk_vao + 1) % 2
        self.ser.write(f'b|{self.dk_vao}\r\n'.encode())
        print("Gửi dữ liệu:", f'b|{self.dk_vao}')
        self.ser.flush()

    def ra(self):
        self.dk_ra = (self.dk_ra + 1) % 2
        self.ser.write(f'c|{self.dk_ra}\r\n'.encode())
        print("Gửi dữ liệu:", f'c|{self.dk_ra}')
        self.ser.flush()

    def thoat(self):
        self.ser.close()
        self.close()

    def closeEvent(self, event):
        self.ser.close()
        event.accept()
    
    def checkCardIdInUser(self, rfid_value):
        url = "http://localhost:8080/smart-parking/users/check-card-id"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "cardId": rfid_value
        }
        
        print(f"Payload: {payload}")  # Debug payload

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                print(f"API Response: {data}")
                if data.get("code") == 1000:
                    user_details = data["result"]
                    print("User Details:", user_details)
                    return user_details  # Trả về thông tin chi tiết người dùng
                else:
                    print(f"Error: {data.get('message')}")
                    return None
            else:
                print(f"HTTP Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error calling API: {e}")
            return None

    def get_available_parking_lot(self):
        url = "http://localhost:8080/smart-parking/users-transient/count-parking-lot"
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"API Response: {data}")  # Debug API response
                if data.get("code") == 1000:
                    return data["result"]  # Trả về dictionary chứa thông tin
                else:
                    print(f"Error: {data.get('message')}")
                    return {"countAll": 0, "countAvailable": 0}  # Giá trị mặc định
            else:
                print(f"HTTP Error: {response.status_code}")
                return {"countAll": 0, "countAvailable": 0}  # Giá trị mặc định
        except Exception as e:
            print(f"Error calling API: {e}")
            return {"countAll": 0, "countAvailable": 0}  # Giá trị mặc định
        
    def find_by_plate_license_number(self, plate):
        url = f"http://localhost:8080/smart-parking/users-transient/find-by-plate-license-number?plate={plate}"
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"API Response: {data}")  # Debug API response
                if data.get("code") == 1000:
                    result = data["result"]                                         
                    print(f"Thông tin biển số xe: {result}")
                    return result  # Trả về danh sách thông tin liên quan đến biển số xe
                else:
                    print(f"Error: {data.get('message')}")
                    return None
            else:
                print(f"HTTP Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error calling API: {e}")
            return None

    def check_card_id_in_user_transient(self, card_id):
        url = "http://localhost:8080/smart-parking/users-transient/check-card-id"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "cardId": card_id
        }

        print(f"Payload: {payload}")  # Debug payload

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                print(f"API Response: {data}")  # Debug API response
                if data.get("code") == 1000:
                    is_valid = data["result"].get("isValidCardId", False)
                    print(f"Is Valid Card ID: {is_valid}")
                    return is_valid  # Trả về True nếu cardId hợp lệ, False nếu không
                else:
                    print(f"Error: {data.get('message')}")
                    return False
            else:
                print(f"HTTP Error: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error calling API: {e}")
            return False