import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from admin_ui import Ui_MainWindow
from Custom_Widgets import *
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        stype_path = r"Qss\admin.qss"
        app.setStyleSheet(Path(stype_path).read_text())
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
            
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())