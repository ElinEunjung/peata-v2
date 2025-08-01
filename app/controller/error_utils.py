"""
Parses TikTok API error responses and maps them to user-friendly messages.

Author: Elin
Date: 2025-06-28
Version: v2.0.0
"""

import json
import re


def get_friendly_error_message(error_text: str, status_code: int = None) -> str:
    # First check HTTP status code
    if status_code == 503:
        return "The server is temporarily unavailable. Please try again after a few minutes."

    # Extract JSON string
    match = re.search(r"\{.*\}", error_text)
    if not match:
        return f"An unexpected error occurred:\n\n{error_text}"

    try:
        error_data = json.loads(match.group(0))
        code = error_data.get("error", {}).get("code", "")

        messages = {
            "rate_limit_exceeded": ("API rate limit exceeded." "Please try again later."),
            "daily_quota_limit_exceeded": ("Daily API quota exceeded." "Please try again later."),
            "internal_error": ("Internal server error." "Please try again later."),
            "invalid_params": (
                "Invalid parameters provided." "Please check your input value is correct and not missing"
            ),
            "access_token_invalid": ("Session expired." "Please log in again to continue."),
            "scope_permission_missed": (
                "Access token missing required scopes." "Please update your access permission and retry."
            ),
            "scope_not_authorized": (
                "You are not authorized for the required scope." "Please authorize access and try again."
            ),
        }

        return messages.get(code, f"TikTok API error: {code}")
    except Exception:
        return f"An unexpected error occurred:\n\n{error_text}"
