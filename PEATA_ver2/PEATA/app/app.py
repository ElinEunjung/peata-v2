import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QIcon

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project PEATA")
        self.resize(900, 900)  # Window size
        
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.jpg")
        self.setWindowIcon(QIcon(icon_path))

        self.center()  # Centre the window on screen
        self.load_stylesheet()

    def load_stylesheet(self):
        qss_path = os.path.join(os.path.dirname(__file__), "style.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r") as file:
                self.setStyleSheet(file.read())
        else:
            print("ERROR> style.qss not found!")

    def center(self):
        frame_geom = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geom.moveCenter(screen_center)
        self.move(frame_geom.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
