import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QStackedWidget, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Import pages
# from page1 import Page1
from page1_copy import Page1Test as Page1
from page2 import Page2
from page3 import Page3
from page4 import Page4

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Xe ra vào")
        self.init_ui()

    def init_ui(self):
        # Main container
        container = QWidget()
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left sidebar
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar")
        sidebar_widget.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Create sidebar buttons
        self.btn1 = QPushButton("Quản Lý Xe Ra - Vào")
        self.btn2 = QPushButton("Đăng Ký Người Dùng")
        self.btn3 = QPushButton("Quản Lý Xe Đang Đỗ")
        self.btn4 = QPushButton("Hỗ Trợ Khách Hàng")
        # self.btn5 = QPushButton("Tổng Quan Bãi Xe")
        
        # Store buttons in a list for easier management
        self.sidebar_buttons = [self.btn1, self.btn2, self.btn3, self.btn4]
        
        # Set object names for styling
        for btn in self.sidebar_buttons:
            btn.setObjectName("sidebarButton")
        
        # Add buttons to sidebar
        sidebar_layout.addWidget(self.btn1)
        sidebar_layout.addWidget(self.btn2)
        sidebar_layout.addWidget(self.btn3)
        sidebar_layout.addWidget(self.btn4)
        # sidebar_layout.addWidget(self.btn5)
        sidebar_layout.addStretch()
        
        # Right content
        content_widget = QWidget()
        content_widget.setObjectName("content")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Header
        header_widget = QWidget()
        header_widget.setObjectName("header")
        header_widget.setFixedHeight(80)
        header_layout = QVBoxLayout(header_widget)
        
        # Header title
        header_title = QLabel("BÃI XE THÔNG MINH")
        header_title.setAlignment(Qt.AlignCenter)
        header_title.setFont(QFont("Arial", 14, QFont.Bold))
        
        header_layout.addWidget(header_title)
        
        # Main content / Stacked Widget for pages
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("contentStack")
        
        # Create pages
        self.page1 = Page1()
        self.page2 = Page2()
        self.page3 = Page3()
        self.page4 = Page4()
        
        # Add pages to stack
        self.content_stack.addWidget(self.page1)
        self.content_stack.addWidget(self.page2)
        self.content_stack.addWidget(self.page3)
        self.content_stack.addWidget(self.page4)
        
        # Footer
        footer_widget = QWidget()
        footer_widget.setObjectName("footer")
        footer_widget.setFixedHeight(60)
        footer_layout = QVBoxLayout(footer_widget)
        
        footer_label = QLabel("ĐỒ ÁN TỐT NGHIỆP - ĐẠI HỌC QUỐC GIA TP.HCM")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setFont(QFont("Arial", 12))
        
        footer_layout.addWidget(footer_label)
        
        # Add widgets to content layout
        content_layout.addWidget(header_widget)
        content_layout.addWidget(self.content_stack, 1)  # Content stack takes remaining space
        content_layout.addWidget(footer_widget)
        
        # Add sidebar and content to main layout
        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(content_widget, 1)  # Content takes remaining space
        
        # Connect buttons to change pages and update active state
        self.btn1.clicked.connect(lambda: self.change_page(0))
        self.btn2.clicked.connect(lambda: self.change_page(1))
        self.btn3.clicked.connect(lambda: self.change_page(2))
        self.btn4.clicked.connect(lambda: self.change_page(3))
        
        # Set active page to first one
        self.change_page(0)
        
        # Set main container as central widget
        self.setCentralWidget(container)
        
        # Load styles
        self.load_styles()
    
    def change_page(self, index):
        """
        Change the active page and update button styles
        """
        # Set current index in stack widget
        self.content_stack.setCurrentIndex(index)
        
        # Gọi load_data() nếu chuyển đến Page3
        if index == 2:  # Page3 nằm ở vị trí thứ 2 trong stack
            self.page3.load_data()

        # Update active states for all buttons
        for i, btn in enumerate(self.sidebar_buttons):
            # Using style property to mark active button
            if i == index:
                btn.setProperty("active", True)
            else:
                btn.setProperty("active", False)
            
            # Force style refresh
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()
        
    def load_styles(self):
        style_path = "admin\styles\layout.qss"
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())
                