import requests
import os
import json
import csv
import logging
from error_utils import get_friendly_error_message

BASE_URL = "https://open.tiktokapis.com/v2"

class TikTokApi:
    #TODO - do not use .env, use variables from user instead
    #Use this in production
    """def __init__(self, client_key, client_secret, access_token):
        self.client_key = client_key
        self.client_secret = client_secret
        #If access_token = None - invalid parameters or something else is wrong
        self.access_token = access_token
        
        self.VIDEO_QUERY_URL = BASE_URL + "/research/video/query/"
        self.USER_INFO_URL = BASE_URL + "/research/user/info/"
        self.VIDEO_COMMENTS_URL = BASE_URL + "/research/video/comment/list/" """
        
        #Using this for testing
    def __init__(self, client_key,client_secret, access_token):
         self.client_key = client_key
         self.client_secret = client_secret
         #If access_token = None - invalid parameters or something else is wrong
         self.access_token = access_token
         
         self.VIDEO_QUERY_URL = BASE_URL + "/research/video/query/"
         self.USER_INFO_URL = BASE_URL + "/research/user/info/"
         self.VIDEO_COMMENTS_URL = BASE_URL + "/research/video/comment/list/"
    

    
    #This method only is able to get username AND keyword, in a EQ operation
    def get_videos(self, username, keyword, startdate, enddate):
        query_params = {
                "fields" : "id,video_description,create_time,region_code,share_count,view_count,like_count,comment_count,music_id,hashtag_names,username,effect_ids,playlist_id,voice_to_text,is_stem_verified,video_duration,hashtag_info_list,video_mention_list,video_label",
                "max_count" : 100,
                "start_date" : startdate,
                "end_date" : enddate
        }
        
        query_body = {
            "query":   {
                    "and" : [{
                            "operation" : "EQ",
                            "field_name" : "keyword",
                            "field_values" : [f"{keyword}"]
                        }, {
                            "operation" : "EQ",
                            "field_name" : "username",
                            "field_values" : [f"{username}"]
                        }]
                },
                "start_date" : startdate,
                "end_date" : enddate,
                "cursor": 0
        }
                            
        headers = {
                "Content-Type" : "application/json",
                "Authorization" : f"Bearer {self.access_token}"
            }
        
        does_have_more = True
        all_videos = []
        cursor = 0
        search_id = None
        while does_have_more:
            query_body["cursor"] = cursor
            if search_id:
                query_body["search_id"] = search_id
                
            response = requests.post(self.VIDEO_QUERY_URL, json=query_body, params=query_params, headers=headers)

            if response.status_code == 200:
                response_json = response.json()
                error = response_json.get("error", {})
                if error.get("code") == "daily_quota_limit_exceeded":
                    print("API quota exceeded. Stopping fetch.")
                    break
                
                data = response_json().get("data", [])
                videos = data.get("videos", [])
                all_videos.extend(videos)
                
                
                if not len(all_videos):
                    print("No videos to return")
                    break
                
                search_id = data.get("search_id", search_id)                
                check_pagination = data["has_more"]
                if check_pagination == False:
                    return all_videos
                
                if "cursor" in data:
                    cursor = data["cursor"]
                else:
                    does_have_more = False
                
            else:
                logging.error("Something went wrong")
                error = response.json()
                return error
            
        print(query_body)
        return all_videos
           
    def get_videos_by_dynamic_query_body(self, query_body, start_date, end_date):
        query_params = {
                "fields" : "id,video_description,create_time,region_code,share_count,view_count,like_count,comment_count,music_id,hashtag_names,username,effect_ids,playlist_id,is_stem_verified,video_duration,hashtag_info_list,video_mention_list,video_label",
                "max_count" : 100,
                "start_date" : start_date,
                "end_date" : end_date
        }
        
        headers = {
                "Content-Type" : "application/json",
                "Authorization" : f"Bearer {self.access_token}"
        }
        
        does_have_more = True
        all_videos = []
        cursor = 0
        search_id = None
        
        while does_have_more:
            query_body["cursor"] = cursor
            
            if search_id:
                query_body["search_id"] = search_id
            response = requests.post(self.VIDEO_QUERY_URL, json=query_body, params=query_params, headers=headers)
            
            if response.status_code == 200:
                data = response.json().get("data", [])
                videos = data.get("videos", [])
                all_videos.extend(videos)
                
                if len(all_videos) == 0:
                    return all_videos
                
                search_id = data.get("search_id", search_id)                
                check_pagination = data["has_more"]
                if check_pagination == False:
                    return all_videos
                
                if "cursor" in data:
                    cursor = data["cursor"]
                else:
                    does_have_more = False
                
            else:
                logging.error("something went wrong")
                error = response.json()
                print(error)
                return error
        
        return all_videos

    #Edge case - extreme long processing time for many comments!
    def get_video_comments(self, video_id):
        url = f"{self.VIDEO_COMMENTS_URL}?fields=id,like_count,create_time,text,video_id,parent_comment_id"
        
        headers = {
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {self.access_token}"
        }
    
        data = {
            "video_id" : video_id,
           "max_count" : 100,
           "cursor": 0
            
        }
        all_comments = []
        
        does_have_more = True
        cursor_count = 0
        while does_have_more:
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                response_json = response.json()
                error = response_json.get("error", {})
                if error.get("code") == "daily_quota_limit_exceeded":
                    print("API quota exceeded. Stopping fetch.")
                    does_have_more = False
                    break
                
                comments_data = response_json.get("data", {})

                comments = comments_data.get("comments", [])
                print(comments)
                if len(comments) < 1:
                    does_have_more = False
                    break
                    
                all_comments.extend(comments)
                

                does_have_more = comments_data.get("has_more", False)
                cursor_count = len(all_comments)
                if does_have_more:
                    data["cursor"] = cursor_count
        
                if not len(all_comments):
                    break
            else:
                logging.error("Something went wrong")
                print("Error response:", response.json())
                break
            
        return all_comments


    def get_public_user_info(self, username):
        url = f"{self.USER_INFO_URL}?fields=display_name,bio_description,avatar_url,is_verified,follower_count,following_count,likes_count,video_count"
        
        headers = {
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {self.access_token}"
        }
        
        data = {
            "username" : username
        }
        
        response = requests.post(url, headers=headers, json=data)
        print(response.json())
        
        if(response.status_code == 200):
            user_info = response.json().get("data", None)
            if not user_info:
                return None
            
            return user_info
        else:
            logging.error("Something went wrong")
            error = response.json()
            return error


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
            "max_count": limit
        }
    
        # JSON body setting
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        
        body = {
            "query": query_body["query"],
            "start_date": start_date,
            "end_date": end_date,
            "max_count": limit,
            "cursor": cursor
            }
        
        if search_id:
            body["search_id"] = search_id
    
        # API Request
        try:
            # print("[DEBUG] ------ API REQUEST START ------")
            # print("[DEBUG] URL:", self.VIDEO_QUERY_URL)
            # print("[DEBUG] Headers:", headers)
            # print("[DEBUG] Query Params:", query_params)
            # print("[DEBUG] Body:", json.dumps(body, indent=2))
            # print("[DEBUG] ------ API REQUEST END ------")
            response = requests.post(
                self.VIDEO_QUERY_URL,
                json=body,
                params=query_params,
                headers=headers
            )
    
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
        url = f"{self.VIDEO_COMMENTS_URL}?fields=id, text, parent_comment_id, like_count, reply_count, create_time"
        
    
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        body = {
            "video_id": video_id,
            "cursor": cursor,
            "max_count": limit
        }

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
    
    
    
    
