import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QSizePolicy, QVBoxLayout, QWidget

from .common_ui_elements import create_button, create_progress_bar


class ProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Fetching data...")
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Label
        self.label = QLabel("Please wait while we fetch your data.")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Progress Bar
        self.progress = create_progress_bar()
        self.progress.setMinimumWidth(300)
        self.progress.setTextVisible(False)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(self.progress)

        # Cancel button using common ui elements
        self.cancel_button = create_button("Cancle", click_callback=self.cancel)
        self.cancel_button.clicked.connect(self.cancel)
        # Cancel Button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.setContentsMargins(0, 10, 0, 0)  # padding-top 10px
        btn_layout.addWidget(self.cancel_button)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self._cancelled = False

        self.adjustSize()

    def cancel(self):
        self._cancelled = True  # Develop this in the future!
        self.close()

    @staticmethod  # avalible to call with class name e.g, PrgressBar.run_with_progress
    def run_with_progress(parent, task_function, on_finished=None):
        """
        Show the progress bar while executing a long-running task.
        - task_function: the function to run
        - on_finished: optional callback to run when done, receives the result
        """
        progress_window = ProgressBar(parent)
        progress_window.center_to_parent()
        progress_window.show()

        def start_work():
            try:
                result = task_function()
            except Exception as e:
                result = e
            finally:
                progress_window.close()
                if isinstance(result, Exception):
                    QMessageBox.critical(parent, "Error", str(result))
                else:
                    if on_finished:
                        on_finished(result)

        QTimer.singleShot(700, start_work)  # slight delay to allow UI to update

    def center_to_parent(self):
        if self.parent():
            parent_geom = self.parent().frameGeometry()
            self_geom = self.frameGeometry()
            center_point = parent_geom.center()
            self_geom.moveCenter(center_point)
            self.move(self_geom.topLeft())


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ProgressBar()
    window.show()
    sys.exit(app.exec_())
