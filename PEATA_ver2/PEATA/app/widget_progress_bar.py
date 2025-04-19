import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt5.QtCore import Qt, QTimer
from widget_common_ui_elements import create_button, create_progress_bar

"""
Progress bar work flow

- Show progress indicator
- Avalible to stop processing (_cancelled = True)
- After processing (fetching data), run callback function (on_finished(result)) 
"""

class ProgressBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fetching data...")
        self.setFixedSize(400, 120)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        
        layout = QVBoxLayout()
        
        
        self.label = QLabel("Please wait while we fetch your data.")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        self.progress = create_progress_bar()
        layout.addWidget(self.progress)
        
        # Cancel button using common ui elements
        self.cancel_button = create_button("Cancle", click_callback=self.cancel)
        self.cancel_button.clicked.connect(self.cancel)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_button)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        self._cancelled = False

        
    def cancel(self):
        self._cancelled = True # Develop this in the future!
        self.close()
        
    @staticmethod # avalible to call with class name e.g, PrgressBar.run_with_progress
    def run_with_progress(parent, task_function, on_finished=None):
        """
        Show the progress bar while executing a long-running task.
        - task_function: the function to run
        - on_finished: optional callback to run when done, receives the result
        """
        progress_window = ProgressBar()
        progress_window.setParent(parent)
        progress_window.setWindowModality(Qt.ApplicationModal)
        progress_window.show()

        def start_work():
            result = None
            if not progress_window._cancelled:
                result = task_function()
            progress_window.close()
            if not progress_window._cancelled and on_finished:
                on_finished(result)

        QTimer.singleShot(100, start_work) # slight delay to allow UI to update
      

  

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ProgressBar()
    window.show()
    sys.exit(app.exec_())
