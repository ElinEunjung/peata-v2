"""
Main application package for PEATA GUI v2, integrating UI, API, and data logic.

Author: Elin
Date: 2025-06-28
Version: v2.0.0
"""

# Expose key classes for external use
__version__ = "2.0.0"
from .model import TikTokApi
from .view import AboutUs, CommentQueryUI, LoginWidget, Navbar, UserInfoQueryUI, VideoQueryUI
