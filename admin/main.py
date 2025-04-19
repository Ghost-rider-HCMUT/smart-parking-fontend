import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from admin import Ui_MainWindow
from Custom_Widgets import *
from pathlib import Path
import json
import requests
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        stype_path = r"admin\Qss\admin.qss"
        app.setStyleSheet(Path(stype_path).read_text(encoding='utf-8'))
        loadJsonStyle(self, self.ui)

        self.set_active_button(self.ui.btn_nav_1)
        # Set Sidebar Menu
        self.ui.btn_nav_1.clicked.connect(lambda: self.change_screen(0, self.ui.btn_nav_1))
        self.ui.btn_nav_2.clicked.connect(lambda: self.change_screen(1, self.ui.btn_nav_2))
        self.ui.btn_nav_3.clicked.connect(lambda: self.change_screen(2, self.ui.btn_nav_3))
        self.ui.btn_nav_4.clicked.connect(lambda: self.change_screen(3, self.ui.btn_nav_4))

        # Set event prev, next btn
        self.ui.btn_prev.clicked.connect(self.handle_prev_page)
        self.ui.btn_next.clicked.connect(self.handle_next_page)

        # Set event logout
        self.ui.btn_logout.clicked.connect(self.show_logout_message)
        
        self.ui.button_register.clicked.connect(self.handle_register)


    # Define function
    # Handle change screen
    def change_screen(self, index, active_button):
        self.ui.pages_list.setCurrentIndex(index)
        self.set_active_button(active_button)
        
    def set_active_button(self, active_button):
        buttons = [self.ui.btn_nav_1, self.ui.btn_nav_2, self.ui.btn_nav_3, self.ui.btn_nav_4]
    
        for btn in buttons:
            if btn == active_button:
                btn.setStyleSheet("""
                    background-color: #fff;
                    border-top-left-radius: 15px;
                    border-bottom-right-radius: 15px;
                """)
            else:
                btn.setStyleSheet("")
    # Handle Prev btn
    def handle_prev_page(self):
        current_index = self.ui.pages_list.currentIndex()
        new_index = (current_index - 1) % 4
        self.ui.pages_list.setCurrentIndex(new_index)
        self.set_active_button(self.get_nav_button(new_index))

    # Handle Next btn
    def handle_next_page(self):
        current_index = self.ui.pages_list.currentIndex()
        new_index = (current_index + 1) % 4  
        self.ui.pages_list.setCurrentIndex(new_index)
        self.set_active_button(self.get_nav_button(new_index))
    
    def get_nav_button(self, index):
        buttons = [self.ui.btn_nav_1, self.ui.btn_nav_2, self.ui.btn_nav_3, self.ui.btn_nav_4]
        return buttons[index]

    # Handle show message logout
    def show_logout_message(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Xác nhận")
        msg_box.setText("Bạn có chắc chắn muốn đăng xuất?")
        msg_box.setIcon(QMessageBox.Question)

        # Add Yes & No
        yes_button = msg_box.addButton("Đồng ý", QMessageBox.YesRole)
        no_button = msg_box.addButton("Hủy", QMessageBox.NoRole)

        # Add CSS (QSS)
        yes_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-size: 14px;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        no_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                font-size: 14px;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)

        msg_box.exec_()
        if msg_box.clickedButton() == yes_button:
            print("Đang đăng xuất...")
            self.close() 
            
    def handle_register(self):
        full_name = self.ui.input_fullname.toPlainText().strip() 
        username = self.ui.input_username.toPlainText().strip() 
        password = self.ui.input_password.toPlainText().strip()  
        confirm_password = self.ui.input_confirm_password.toPlainText().strip() 
        phone_number = self.ui.input_phone.toPlainText().strip() 
        months = self.ui.input_months.toPlainText().strip()
        location_id = self.ui.input_location.toPlainText().strip()  
        license_plate = self.ui.input_plate.toPlainText().strip()
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
            response = requests.post(
                "https://64ea-42-118-214-203.ngrok-free.app/smart-parking/users", 
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )
        
            if response.status_code == 200:
                print("Đăng ký thành công:", response.json())
                self.clear_form() 
                self.show_message_box("Đăng ký người dùng mới thành công!", True)
            else:
                print("Lỗi:", response.status_code, response.text)
                self.show_message_box("Đăng ký không thành công!", False)

        except Exception as e:
             print("Lỗi khi gọi API:", e)
             
    def clear_form(self):
        self.ui.input_fullname.clear()
        self.ui.input_username.clear()
        self.ui.input_password.clear()
        self.ui.input_confirm_password.clear()
        self.ui.input_phone.clear()
        self.ui.input_location.clear()
        self.ui.input_months.clear()
        self.ui.input_plate.clear()
        
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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())