import json
import re

def get_friendly_error_message(error_text: str) -> str:
    # Extract JSON string 
    match = re.search(r'\{.*\}', error_text)
    if not match:
        return f"An unexpected error occurred:\n\n{error_text}"

    try:
        error_data = json.loads(match.group(0))
        code = error_data.get("error", {}).get("code", "")

        messages = {
            "rate_limit_exceeded": "API rate limit reached. Please try again later.",
            "daily_quota_limit_exceeded": "Daily API quota exceeded. Try again later.",
            "internal_error": "Server error. Please try again later.",
            "invalid_params": "Please check that the username and keyword combination actually exists during the selected date range."
        }

        return messages.get(code, f"TikTok API error: {code}")
    except Exception:
        return f"An unexpected error occurred:\n\n{error_text}"
    
    
# # For testing
# if __name__ == "__main__":
#     test_msg = 'TikTok API Error:, 429, {"data":{},"error":{"code":"daily_quota_limit_exceeded","message":"The API daily quota limit exceeded. Please try again later"}}'
#     print(get_friendly_error_message(test_msg))