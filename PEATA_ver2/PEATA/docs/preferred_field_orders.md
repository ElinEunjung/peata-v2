# 📊 Preferred Field Orders in PEATA

This document explains the default field ordering used when displaying or exporting TikTok data in PEATA.  
The field order is designed to optimize researcher experience, ensuring that the most relevant information appears first.



## 🟢 Comment Data: `preferred_order_comment`

This field order is designed for efficient readability and analytical relevance. The most meaningful and human-facing information is placed first.

```python
[
    "text",
    "like_count",
    "reply_count",
    "create_time",
    "id",
    "parent_comment_id",
    "video_id"
]
```

**Field Meanings:**

- **text** – Content of the comment; primary subject for textual or sentiment analysis.
- **like_count** – Shows popularity and engagement.
- **reply_count** – Reflects conversational depth.
- **create_time** – For timeline analysis or sorting.
- **id** – Unique comment ID (reference purposes).
- **parent_comment_id** – Shows if this is a reply to another comment.
- **video_id** – Identifier for the related video.



## 🔵 Video Data: `preferred_order_video`

This order groups fields by their relevance: from basic identifiers to performance metrics, and finally content composition.

```python
[
    "id", "username", "region_code", "create_time",
    "video_description", "video_duration",
    "view_count", "like_count", "comment_count", "share_count",
    "music_id", "playlist_id",
    "hashtag_names", "hashtag_info_list",
    "effect_ids", "effect_info_list",
    "voice_to_text", "video_mention_list",
    "video_label", "video_tag", "is_stem_verified",
    "sticker_info_list"
]
```

**Field Groupings:**

- **Top section** – Identity and creation metadata (e.g. username, region, time)
- **Middle** – Performance metrics and user-facing content
- **Bottom** – Hashtags, effects, AI-labeled fields, and visuals

---

## 🔷 User Info: `preferred_order_userinfo`

The ordering helps quickly identify the user and assess their influence.

```python
[
    "username", "display_name", "bio_description",
    "avatar_url", "is_verified",
    "follower_count", "following_count", "likes_count", "video_count"
]
```

**Order Logic:**

1. **Who is this?** – `username`, `display_name`
2. **How do they present themselves?** – `bio`, `avatar`, `is_verified`
3. **How influential are they?** – `follower_count`, `likes_count`, `video_count`

---

📝 Note: This order only affects how data is **displayed** or **exported** (e.g., CSV/Excel). It does **not** change the raw API response.