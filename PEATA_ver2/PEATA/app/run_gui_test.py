from token_manager import obtain_access_token
from api import TikTokApi
from widget_video_query_ui import VideoQueryUI
# from widget_userinfo_query_ui import UserInfoQueryUI
from widget_comment_query_ui import CommentQueryUI

from PyQt5.QtWidgets import QApplication
import sys

# Load from .env
import os
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # move from app/ → root
load_dotenv(os.path.join(BASE_DIR, ".env"))

CLIENT_KEY = os.getenv("CLIENT_KEY")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def run_gui(gui_class):
    print(" ✅ run_gui() is running! ") 
    print(f"CLIENT_KEY: {CLIENT_KEY}")
    print(f"CLIENT_SECRET: {CLIENT_SECRET}")
    
    access_token = obtain_access_token(CLIENT_KEY, CLIENT_SECRET)
    print("ACCESS TOKEN:", access_token)
  
    
    access_token = obtain_access_token(CLIENT_KEY, CLIENT_SECRET)

    if not access_token:
        print("❌ Failed to obtain access token")
        return

    app = QApplication(sys.argv)
    
    # Apply style.qss   
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
        
    api = TikTokApi(CLIENT_KEY, CLIENT_SECRET, access_token)
    window = gui_class(api=api)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Run only the UI I want to test
     run_gui(VideoQueryUI)
    # run_gui(UserInfoQueryUI)
    # run_gui(CommentQueryUI)