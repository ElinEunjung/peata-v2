# PEATA Project - Known Server Behavior and Debugging Guide

## 1. API Documentation vs Server Behavior Mismatch

Although the official TikTok Research API documentation specifies various fields as supported for the `/research/video/query/` endpoint (e.g., `favourites_count`), our testing through direct curl requests revealed discrepancies:

- Some fields listed in the documentation (e.g., `favourites_count`) are **not actually accepted by the server**.
- If such unsupported fields are included in the `fields` parameter, the server responds with an `invalid_params` error.

### Action Taken:
- We have **removed** unsupported fields like `favourites_count` from both the GUI field list and the preferred field order used internally.
- The system is designed to **trust actual server behavior over documentation listings** for maximum stability.

### Important Note:
- Even if a field is listed in the documentation, it should be **independently verified** against the live server behavior before use.


## 2. Debugging Guide for API Requests (Using curl)

When encountering unexplained API errors such as `invalid_params`, the most reliable way to debug is by sending a direct `curl` request to the API endpoint.

### Step-by-Step Debugging Process:

1. **Prepare your curl command** matching exactly what your client sends:

```bash
curl -X POST "https://open.tiktokapis.com/v2/research/video/query/?fields=id,username,..." \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "query": {
    "and": [
      { "operation": "EQ", "field_name": "username", "field_values": ["example_username"] },
      { "operation": "EQ", "field_name": "keyword", "field_values": ["example_keyword"] }
    ]
  },
  "start_date": "YYYYMMDD",
  "end_date": "YYYYMMDD",
  "max_count": 100,
  "cursor": 0
}'
```

2. **Send the request and analyze the server's raw response:**
   - If the response shows an `invalid_params` error, check if any field in the `fields` list is unsupported.
   - If the response is successful but returns empty data, it means the query structure is correct but no matching data was found.

### Best Practices:
- Always **minimize** the payload first (e.g., just `id`, `username`) and then **gradually add fields** to identify which field might cause problems.
- If unsure about a field, remove it and retest.
- Trust the **server's response behavior over documentation** during debugging.



## 3. Conclusion

- **Code structure issues** and **invalid query formats** were ruled out.
- **Server-side field support mismatch** caused `invalid_params` errors.
- **Direct curl testing** proved to be the most reliable debugging method.
- Our system is now built to handle such server inconsistencies safely.



*Document Last Updated: 2025-04-27*

