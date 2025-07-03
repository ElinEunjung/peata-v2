# TikTok Research API Codebook Summary

This document provides a concise overview of the datasets made available via TikTok's Research API. It is intended to help researchers quickly understand the **unit of analysis**, **data scope**, and **key fields** available for each endpoint.

---

## 1. Video Dataset

- **Unit of Analysis**: A public TikTok video posted by a public creator (aged 18+).
- **Scope**:
  - The video must be publicly visible.
  - The creator must be 18 years or older.
  - The creator must not be based in Canada.
  - Only videos posted from the following regions are included:
    - United States (US)
    - Europe
    - Rest of the World (excluding Canada)

### Available Fields
See: [`fields-video.md`](./fields-video.md) for the full list of video fields and their descriptions.

---

## 2. Comment Dataset

- **Unit of Analysis**: A comment or reply posted on a public TikTok video.

### Available Fields
| Field Name           | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `text`               | Text content of the comment.                                                |
| `like_count`         | Number of likes the comment has received.    
| `create_time`        | Timestamp when the comment was created.                                     |
| `id`                 | Unique identifier for the comment.                                                        |
| `reply_count`        | Number of replies under this comment.                                       |
| `parent_comment_id`  | ID of the parent comment, or the video ID if it's a top-level comment.      |
| `video_id`           | ID of the video the comment belongs to.                                     |

---

## 3. User Dataset

- **Unit of Analysis**: A TikTok user account that is public and belongs to a person aged 18 or older.

### Available Fields
| Field Name           | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `username`           | The user’s unique TikTok handle.                                            |
| `display_name`       | The user's profile name (distinct from username).                           |
| `bio_description`    | Text from the user's bio. Blank if not provided.                            |
| `avatar_url`         | URL of the user’s profile picture.                                          |
| `is_verified`        | Whether the user has a verification badge (blue tick).                      |
| `follower_count`     | Total number of followers.                                                  |
| `following_count`    | Number of other users this account follows.                                 |
| `likes_count`        | Total number of likes the user has received across their content.           |
| `video_count`        | Total number of videos posted by the user.                                  |


---

**Note**: 
1. Field order matches export output. No separate fields-comment.md or fields-user.md is needed.
2. All datasets only contain information from public accounts and content that adheres to TikTok's research access policies.


> Source: <br>
> [TikTok Research API Codebook](https://developers.tiktok.com/doc/research-api-codebook) 
