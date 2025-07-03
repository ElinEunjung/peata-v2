# 📘 PEATA App Usage Guide

## 🚀 Getting Started

1. **Launch** the PEATA desktop app.
2. **Sign in** with valid TikTok Research API credentials.
3. **Choose a query type** from the left navigation menu:

   * Video Query
   * Comment Query
   * User Info Query

---

## 🔍 Running a Video Query

### 1. Select Fields

- All fields are checked by default.
- You may uncheck fields to exclude them from the query result.
- Fields are grouped as:
  * Creator Info (Id, Username etc.)
  * Posting info (Create Time, Video duration etc.)
  * Engagement (View Count, Like Count etc.)
  * Tags Metadata (Hashtag Names, Video Label etc.)
  * Advanced Fields (Effect Ids, Hashtag Info list etc)
* See full list in [TikTok Video Fields Reference Guide](fields-video.md). 
  
### 2. Set Filters
- Filters can be set using the **Filter Builder Section** *(Filter Condition to apply)*.
- Each filter row must include:
  * Field name
  * Operation (EQ, IN, GT, etc.)
  * Field values (comma-separated)
- Click **Add** for values like `region_code`.
- Use logical groups: **AND**, **OR**, **NOT**

> ⚠️ `end_date` must be within **30 days after** `start_date` <br>
> 💡 See [TikTok Video Filter Guide](video-filter-guide.md) for detailed filter information. <br>
> 💡 See [Query Best Practice Tips](query-best-practices.md) for filter examples <br>

### 3. Live Query Preview

- Automatically shows the JSON structure of your query.
- Use it to verify structure before clicking **Run Query**.

---

## 📦 Fetching Data

1. **Choose Max Results** (default: 500)
   - Values over 1000 may trigger quota limits or API failure.
2. **Click "Run Query"**
   - Results will appear in a table if successful.
   - If a query fails, descriptive error messages will appear in dialog pop-ups.
3. **Click "Load More"** for paginated results (Up to 100 per page)
> Duo to private setting or user age (under 18), it might not fetch 100 rows at a time.

---

## 💾 Exporting Data

- Click **Export** to save data as `.csv` or `.xlsx`
- A progress bar will show during export.
- Large exports may appear *frozen* but are processing.
- Messages confirm success/failure.

  
### Export Location

- `data/csv/` for CSV
- `data/excel/` for Excel
> In the case of API failure, partial downloaded data will be exported. 

---
## 📚 Related Docs

- [TikTok Video Fileds Reference Guide](./fields-video.md)
- [TikTok Video Filter Guide](./video-filter-guide.md) <br>
- [TikTok API Codebook Summary](./codebook-summary.md)
- [Query Design Best Practice](./query-best-practices.md) *(coming soon)* <br>
