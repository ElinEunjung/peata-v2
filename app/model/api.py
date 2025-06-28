import requests

from app.controller.error_utils import get_friendly_error_message

BASE_URL = "https://open.tiktokapis.com/v2"


class TikTokApi:

    def __init__(self, client_key, client_secret, access_token):
        self.client_key = client_key
        self.client_secret = client_secret
        self.access_token = access_token

        self.VIDEO_QUERY_URL = BASE_URL + "/research/video/query/"
        self.USER_INFO_URL = BASE_URL + "/research/user/info/"
        self.VIDEO_COMMENTS_URL = BASE_URL + "/research/video/comment/list/"

    # Added for Gui v.2 - Video (Advanced mode) with pagination
    def fetch_videos_query(self, query_body, start_date, end_date, cursor=0, limit=100, search_id=None):

        # Check Mush-have Fields
        fields = query_body.get("fields")
        if not fields or not isinstance(fields, list) or len(fields) == 0:
            raise ValueError("❗ 'fields' are required in query_body and must contain at least one field.")

        query = query_body.get("query")
        if not query:
            raise ValueError("❗ 'query' structure is missing in query_body.")

        # URL params setting
        query_params = {
            "fields": ",".join(fields),
            "start_date": start_date,
            "end_date": end_date,
            "max_count": limit,
        }

        # JSON body setting
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        body = {
            "query": query_body["query"],
            "start_date": start_date,
            "end_date": end_date,
            "max_count": limit,
            "cursor": cursor,
        }

        if search_id:
            body["search_id"] = search_id

        # API Request
        try:
            response = requests.post(self.VIDEO_QUERY_URL, json=body, params=query_params, headers=headers)

            if response.status_code == 200:
                data = response.json().get("data", {})
                videos = data.get("videos", [])
                has_more = data.get("has_more", False)
                new_cursor = data.get("cursor", 0)
                new_search_id = data.get("search_id", None)

                print(f"✅ API returned {len(videos)} videos (cursor={cursor})")
                return videos, has_more, new_cursor, new_search_id

            else:
                # rasie error
                user_friendly = get_friendly_error_message(response.text, status_code=response.status_code)
                raise Exception(user_friendly)

        except Exception as e:
            raise Exception(f"API request failed: {str(e)}")

    # Added for Gui v.2 - Comment (Simple mode) with pagination
    def fetch_comments_basic(self, video_id, cursor=0, limit=100):
        url = f"{self.VIDEO_COMMENTS_URL}" "?fields=id, text, parent_comment_id, like_count," "reply_count, create_time"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        body = {"video_id": video_id, "cursor": cursor, "max_count": limit}

        try:
            response = requests.post(url, headers=headers, json=body)
            print("=== [DEBUG] Raw Response JSON ===")
            print(response.json())

            if response.status_code == 200:
                res_json = response.json()
                data = res_json.get("data", {})
                comments = data.get("comments", [])
                has_more = data.get("has_more", False)
                new_cursor = data.get("cursor", cursor)
                return comments, has_more, new_cursor, None

            else:
                error_msg = f"API Error {response.status_code}: {response.text}"
                user_friendly = get_friendly_error_message(error_msg)
                return [], False, cursor, user_friendly

        except Exception as e:
            user_friendly = get_friendly_error_message(str(e))
            return [], False, cursor, user_friendly

    # Shared code with Gui ver.1
    def get_public_user_info(self, username):
        url = (
            f"{self.USER_INFO_URL}"
            "?fields=display_name,bio_description,avatar_url,is_verified,"
            "follower_count,following_count,likes_count,video_count"
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        data = {"username": username}

        response = requests.post(url, headers=headers, json=data)
        print(response.json())

        if response.status_code == 200:
            user_info = response.json().get("data", None)
            if not user_info:
                return None

            return user_info
        else:
            error = response.json()
            print(f"Error: Failed to fetch user info. {error}")
            return None
