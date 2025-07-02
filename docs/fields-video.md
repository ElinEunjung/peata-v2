# 📄 TikTok Video Field Reference Guide

Full list of video fields available through the Research API.
The order below matches the field layout in the **"Fields to include in result"** panel of the PEATA Video Query interface.
\

| Field Name          | Description |
|---------------------|-------------|
| id                  | Unique video ID |
| username            | Creatorâ€™s TikTok handle |
| region_code         | Country where the account was registered |
| is_stem_verified    | Whether the video is verified as high-quality STEM content |
| create_time         | When the video was created (Unix timestamp) |
| video_duration      | Duration of the video in seconds |
| video_description   | Text description of the video |
| music_id            | ID of the music used in the video |
| playlist_id         | Playlist ID (if the video belongs to a playlist) |
| view_count          | Number of times the video has been viewed|
| like_count          | Number of likes on the video |
| comment_count       | Number of comments under the video |
| share_count         | Number of shares |
| hashtag_names       | List of hashtags used in the video |
| video_label         | Informational labels (e.g., election info) |
| video_tag           | Numeric tag for special video types. (e.g., AI-generated, paid promotion, creator commission.) |
| voice_to_text       | Auto-generated captions (if available) |
| video_mention_list  | List of users tagged in video |
| effect_ids          | List of effect IDs applied to the video |
| effect_info_list    | Metadata for the applied effects |
| hashtag_info_list   | hashtags metadata (id, description) |
| sticker_info_list   | Metadata for interactive stickers |

> ℹ️ Note: 
> `video_tag` values are numeric codes. Categories may be updated by TikTok in the future. 
> See the [TikTok Video Query Spec](https://developers.tiktok.com/doc/research-api-specs-query-videos/)
 
> Sources <br>
> [TikTok Research API Codebook](https://developers.tiktok.com/doc/research-api-codebook) <br>
> [TikTok Research API Specs - Query Videos](https://developers.tiktok.com/doc/research-api-specs-query-videos/)

