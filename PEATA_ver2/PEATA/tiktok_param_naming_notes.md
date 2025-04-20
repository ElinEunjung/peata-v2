# ⚠️ Parameter Naming in TikTok Research API: `max_count` vs `limit`

While working with TikTok's Research API, it's important to note that the same concept—limiting the number of results—is referred to using different parameter names across endpoints.

---

## 🔹 Video API uses: `max_count`

For all video-related queries (e.g., `/v2/research/video/query/`), the number of results returned is controlled by the `max_count` parameter, which must be included in the JSON request body.

```json
{
  "query": { ... },
  "start_date": "20240101",
  "end_date": "20240131",
  "cursor": 0,
  "max_count": 100
}
```

---

## 🔹 Comment API uses: `limit`

For all comment-related queries (e.g., `/v2/research/video/comment/list/`), the limit is set using the `limit` parameter, also inside the JSON body.

```json
{
  "video_id": "1234567890",
  "cursor": 0,
  "limit": 100
}
```

---

## ❗ Why the inconsistency?

This is due to TikTok's internal API systems having different conventions for different resource types. The Research API combines them under one interface but does not normalize the parameter names.

---

## ✅ Best Practice

- Use the parameter name exactly as specified in the endpoint documentation.
- For video queries: use `max_count`
- For comment queries: use `limit`
- Avoid trying to unify or rename these internally, as it may break functionality.

📝 Always refer to the latest [TikTok API documentation](
https://developers.tiktok.com/doc/research-api-specs-query-videos/,
https://developers.tiktok.com/doc/vce-query-video-comments?enter_method=left_navigation) for updates.
