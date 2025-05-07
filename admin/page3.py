import os
import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import requests
from datetime import datetime


class Page3(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("page3")
        self.initUI()
        self.load_styles()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Tiêu đề
        title_label = QLabel("Quản lý dữ liệu")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        main_layout.addWidget(title_label)

        # Search form
        search_layout = QHBoxLayout()
        search_label = QLabel("Tìm kiếm theo:")
        self.search_combo = QComboBox()
        self.search_combo.addItems(["Biển số"])  # Giữ đơn giản theo API đang dùng

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập biển số...")

        search_button = QPushButton("Tìm kiếm")
        search_button.clicked.connect(self.search_data)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_combo)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)

        # Bảng dữ liệu
        self.data_table = QTableWidget(0, 3)
        self.data_table.setHorizontalHeaderLabels(["ID", "Biển số", "Thời gian vào"])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.data_table)

        # Load dữ liệu ban đầu
        self.load_data()

    def load_data(self):
        """Load toàn bộ dữ liệu từ API"""
        try:
            url = os.getenv("HOST") + "/users-transient/get-all-user-transient"
            print(url)
            response = requests.post(url)
            data = response.json().get("result", [])
            self.populate_table(data)
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {e}")
            self.data_table.setRowCount(0)
            
    def on_show(self):
        """Phương thức được gọi mỗi khi Page3 được hiển thị"""
        self.load_data()
    def search_data(self):
        """Tìm kiếm dữ liệu theo biển số"""
        plate = self.search_input.text().strip()
        if not plate:
            self.load_data()
            return

        try:
            url = os.getenv("HOST") + "/users-transient/find-by-plate-license-number"
            response = requests.post(url, params={"plate": plate})
            if response.status_code == 200:
                result = response.json().get("result", [])
                self.populate_table(result)
            else:
                print(f"Lỗi API: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Lỗi khi gọi API: {e}")

    def populate_table(self, data):
        """Hiển thị dữ liệu trong bảng"""
        self.data_table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.data_table.insertRow(row_idx)
            self.data_table.setItem(row_idx, 0, QTableWidgetItem(str(row_data.get("id", ""))))
            self.data_table.setItem(row_idx, 1, QTableWidgetItem(str(row_data.get("plateLicenseNumber", ""))))
            
            # Format thời gian vào
            raw_time = row_data.get("timeStart", "")
            try:
                dt = datetime.fromisoformat(raw_time)
                formatted_time = dt.strftime("%d/%m/%Y %H:%M")
            except:
                formatted_time = raw_time

            self.data_table.setItem(row_idx, 2, QTableWidgetItem(formatted_time))

    def load_styles(self):
        style_path = "admin/styles/page3.qss"
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
