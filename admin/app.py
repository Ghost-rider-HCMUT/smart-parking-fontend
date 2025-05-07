import sys
from PyQt5.QtWidgets import QApplication
from layout import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setFixedSize(1530, 850)  
    window.show()
    sys.exit(app.exec_())
     