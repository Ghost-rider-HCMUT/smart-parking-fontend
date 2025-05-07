import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Page4(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("page4")
        self.init_ui()
        self.load_styles()
        
    def init_ui(self):
        # Main layout
        layout = QVBoxLayout(self)
        
        # Page title
        title = QLabel("Page 4")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setObjectName("pageTitle")
        
        # Add content to layout
        layout.addWidget(title)
        layout.addStretch()
        
        # Description label
        description = QLabel("This is Page 4 content. You can customize this page later.")
        description.setAlignment(Qt.AlignCenter)
        description.setObjectName("description")
        
        layout.addWidget(description)
        layout.addStretch()
        
    def load_styles(self):
        style_path = "admin\styles\page4.qss"
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())