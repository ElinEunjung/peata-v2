# 📄 TikTok Video Field Reference Guide

Full list of video fields available through the Research API.

| Field Name          | Description |
|---------------------|-------------|
| id                  | Unique video ID |
| username            | Creator’s TikTok handle |
| region_code         | Country where the account was registered |
| is_stem_verified    | Boolean: high-quality STEM content |
| create_time         | When the video was created (Unix timestamp) |
| video_duration      | Duration in seconds |
| video_description   | Text description of the video |
| music_id            | ID of music used |
| playlist_id         | Playlist ID (if video belongs to a playlist) |
| view_count          | Number of views |
| like_count          | Number of likes |
| comment_count       | Number of comments |
| share_count         | Number of shares |
| hashtag_names       | List of hashtags used |
| video_label         | Labels like "election info" |
| video_tag           | Numeric tag for special video types. (e.g., AI-generated, paid promotion, creator commission.) |
| voice_to_text       | Auto-generated captions if available |
| video_mention_list  | Other users tagged in video |
| effect_ids          | List of effect IDs applied |
| effect_info_list    | Detailed effect metadata |
| hashtag_info_list   | Additional info on hashtags (id, description) |
| sticker_info_list   | Info on interactive stickers |

> Note: 
> `video_tag` values are numeric codes. Categories may be updated by TikTok in the future. 
> See the [TikTok Video Query Spec](https://developers.tiktok.com/doc/research-api-specs-query-videos/)
 
> Sources <br>
> [TikTok Research API Codebook](https://developers.tiktok.com/doc/research-api-codebook)
> [TikTok Research API Specs – Query Videos](https://developers.tiktok.com/doc/research-api-specs-query-videos/)

