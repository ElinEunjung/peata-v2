"""Main application package for PEATA v2, integrating UI, API, and data logic."""

# Expose key classes for external use
__version__ = "2.0.0"
from .model import TikTokApi
from .view import AboutUs, CommentQueryUI, LoginWidget, Navbar, UserInfoQueryUI, VideoQueryUI
