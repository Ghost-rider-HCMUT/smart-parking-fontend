import json
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QComboBox, QPushButton, QFormLayout,
                           QGridLayout, QFrame, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import requests
from dotenv import load_dotenv

load_dotenv()
class Page2(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("page2")
        self.init_ui()
        self.load_styles()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("ĐĂNG KÝ NGƯỜI DÙNG MỚI")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))

        # Form container
        form_container = QWidget()
        form_container.setFixedSize(600, 600) 
        form_container.setObjectName("formContainer")
        form_layout = QFormLayout(form_container)
        form_layout.setContentsMargins(10, 20, 10, 20)
        form_layout.setSpacing(15)

        # Form fields
        self.name_input = QLineEdit()
        self.name_input.setFont(QFont("Arial", 14))
        self.name_input.setObjectName("nameInput")
        form_layout.addRow("Họ Và Tên", self.name_input)

        self.username_input = QLineEdit()
        self.username_input.setObjectName("usernameInput")
        self.username_input.setFont(QFont("Arial", 14))
        form_layout.addRow("Tên Đăng Nhập", self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setObjectName("passwordInput")
        self.password_input.setFont(QFont("Arial", 14))
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Mật Khẩu", self.password_input)

        self.confirm_input = QLineEdit()
        self.confirm_input.setObjectName("confirmInput")
        self.confirm_input.setFont(QFont("Arial", 14))
        self.confirm_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Xác nhận", self.confirm_input)

        self.phone_input = QLineEdit()
        self.phone_input.setObjectName("phoneInput")
        self.phone_input.setFont(QFont("Arial", 14))
        form_layout.addRow("Số Điện Thoại", self.phone_input)

        self.position_combo = QComboBox()
        self.position_combo.setObjectName("positionCombo")
        self.position_combo.setFont(QFont("Arial", 14))
        self.get_available()
        form_layout.addRow("Vị Trí", self.position_combo)

        self.license_input = QLineEdit()
        self.license_input.setObjectName("licenseInput")
        self.license_input.setFont(QFont("Arial", 14))
        self.license_input.setPlaceholderText("")
        form_layout.addRow("Biển Số Xe", self.license_input)

        self.month_combo = QComboBox()
        self.month_combo.setObjectName("monthCombo")
        self.month_combo.setFont(QFont("Arial", 14))
        self.month_combo.addItems(["1", "2", "3", "6", "12"])
        form_layout.addRow("Số Tháng", self.month_combo)

        # Register button container for centering
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)

        # Register button
        register_button = QPushButton("ĐĂNG KÝ")
        register_button.setObjectName("registerButton")
        register_button.setFixedSize(120, 40)
        register_button.clicked.connect(self.handle_register)

        # Add button to layout with spacing for centering
        button_layout.addStretch()
        button_layout.addWidget(register_button)
        button_layout.addStretch()

        # Add all widgets to main layout
        main_layout.addWidget(title_label)
        
        # New: Center the form_container
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(form_container)
        center_layout.addStretch()

        main_layout.addLayout(center_layout)
        main_layout.addWidget(button_container)

    def handle_register(self):
        full_name = self.name_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_input.text()
        phone_number = self.phone_input.text()
        location_id = self.position_combo.currentText()
        license_plate = self.license_input.text()
        months = self.month_combo.currentText()
        errors = []
        if not full_name:
            errors.append("Họ và tên không được để trống!")
        if not username:
            errors.append("Tên đăng nhập không được để trống!")
        if not password:
            errors.append("Mật khẩu không được để trống!")
        if not confirm_password:
            errors.append("Xác nhận mật khẩu không được để trống!")
        if not phone_number:
            errors.append("Số điện thoại không được để trống!")
        if not location_id:
            errors.append("Vị trí không được để trống!")
        if not license_plate:
            errors.append("Biển số xe không được để trống!")
            
        if errors:
            self.show_message_box(errors[0], False)
            return
    
        if password != confirm_password:
            self.show_message_box("Mật khẩu không khớp!", False)
            return
        
        if len(phone_number) != 10:
            self.show_message_box("Số điện thoại không hợp lệ!", False)
            return
        
        payload = {
            "fullName": full_name,
            "username": username,
            "password": password,
            "confirmPassword": confirm_password,
            "phoneNumber": phone_number,
            "rentalLocation": location_id,
            "months": months,
            "licensePlateNumber": license_plate
        }

        try:
            url = os.getenv("HOST") + "/users"
            response = requests.post(
                url, 
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )
        
            if response.status_code == 200:
                print("Đăng ký thành công:", response.json())
                self.clear_form() 
                self.show_message_box("Đăng ký người dùng mới thành công!", True)
                self.get_available()
            else:
                print("Lỗi:", response.status_code, response.text)
                self.show_message_box("Đăng ký không thành công!", False)

        except Exception as e:
             print("Lỗi khi gọi API:", e)
             
    def clear_form(self):
        self.name_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_input.clear()
        self.phone_input.clear()
        self.position_combo.setCurrentIndex(0)
        self.license_input.clear()
        self.month_combo.setCurrentIndex(0)
         
    def show_message_box(parent, message: str, is_success: bool):
        msg_box = QMessageBox(parent)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        ok_button = msg_box.button(QMessageBox.Ok)
        if is_success:
            msg_box.setStyleSheet("QLabel { color: green; font-weight: bold; }")
            msg_box.setWindowTitle("Thành công")
            msg_box.setIcon(QMessageBox.Information)
            ok_button.setStyleSheet("""
                background-color: green; 
                color: white; 
                font-weight: bold; 
                padding: 5px 10px; 
                border-radius: 2px;  
            """)
        else:
            msg_box.setStyleSheet("QLabel { color: red; font-weight: bold; }")
            msg_box.setWindowTitle("Thất bại")
            msg_box.setIcon(QMessageBox.Critical)
            ok_button.setStyleSheet("""
                background-color: red; 
                color: white; 
                font-weight: bold; 
                padding: 5px 10px;
                border-radius: 2px;  
            """)

        # Hiện lên hộp thoại
        msg_box.show()

    def load_styles(self):
        style_path = "admin/styles/page2.qss"
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())
                
    def get_available(self):
        self.position_combo.clear()
        api_url = os.getenv("HOST") + "/parking-lot/available"
        
        try:
            response = requests.post(api_url)
            if response.status_code == 200:
                data = response.json()
                parking_lots = data.get("result", [])  # Dữ liệu nằm trong trường 'result'

                if parking_lots:
                    for lot in parking_lots:
                        lot_id = lot.get("id")
                        if lot_id:  
                            self.position_combo.addItem(lot_id)
                else:
                    self.position_combo.addItem("Không Có Vị Trí Trống")
            else:
                print(f"API call failed with status code: {response.status_code}")
                self.position_combo.addItem("Không Có Vị Trí Trống")

        except Exception as e:
            print(f"Error when calling API: {e}")
            self.position_combo.addItem("Không Có Vị Trí Trống")
