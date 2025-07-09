# 🧼 Query Design Best Tips for PEATA TikTok API - Video

This guide summarizes best practices for building efficient, effective queries using TikTok’s Research API (Video), as tested and validated in the PEATA project.

> 🔗 Full test details are available in [query-test-log.md](./query-test-log.md)

---

## ✅ General Principles

* **`start date` - `end date`** are mandatory parameters
* **Start simple**: Always begin with 1 or 2 filters and check the size/performance.
* **Respect the 30-day limit**: API rejects date ranges longer than 30 days.
* **Field selection matters**: Only include fields needed for analysis to speed up response.
* **Field deselection hides values** in response but columns still exist *(null-filled)* - need to be fixed.
* **Use `Add` button wisely**: In GUI, always click `Add` after changing filter values for `region_code` and `video_length`.

---

## ⚙️ Field-Specific Tips

### `video_id` 
* Officially supported as a filter 
* In practice, often returns no results even when video is known to exist
* Must include start_date and end_date — required even for specific IDs
* Not reliable for fetching a known video
* If no result: test `keyword` or `username` first to find related content


### `keyword`

* Works alone, returns results
* Use for simple topical queries
* comma-separated values increace result volume (change operation to `IN` from `Equals`)
* Combine with narrow date range if result volume is too high


### `username`

* Use full, exact TikTok username
* Results vary significantly


### `region_code`

* Comma-separated multiple values work well (Need to change operation to IN from Equals)
* Use with keywords to regionalize results
* High-volume regions (e.g., `US`) can overwhelm API — narrow by date


### `video_length`

* Supports values: `SHORT`, `MID`, `LONG`, `EXTRA_LONG`
* Combine multiple via `OR`


### `music_id` / `effect_id` 

* Officially supported
* Often return no results
* Use only in combination with other filters like `create_date`, `region_code`


### `create_date`

* Supports `EQ`, `GT`, `LT`, `GTE`, `LTE`
* Use `GT`, `LT` for fine-grained time slicing
* Type date with YYYYMMDD form

---

## 🧪 Known Filter Limitations
Some filters appear supported in documentation but do not reliably return results in practice:

###`video_id`, `music_id`, `effect_id`
* Officially supported
* Often return no results even when values are correct
* `start_date` and `end_date` are still required
* Must be combined with `region_code` or similar
* API may not support direct lookup by ID

---

## 🔄 Logical Operators

* `AND`: All conditions must match (e.g., `region_code + keyword`)
* `OR`: At least one condition must match (e.g., multiple `video_length`)
* `NOT`: Excludes matching conditions (e.g., exclude `hashtag_name: mukbang`)
* **Combine for precision**: `AND + OR + NOT` helps balance volume and focus

---

## 🛑 Common Pitfalls

* ❌ **Date range > 30 days** → invalid\_params error
* ❌ Changing field values without `Add` click in UI → query not updated
* ❌ Broad region + popular keyword → API timeout / partial data

---

## 📁 Field Set Strategy

* Use minimum field set for performance (e.g., `username`, `region`, `keyword` `video_duration`)

> See [TikTok Video Filter Guide](./video-filter-guide.md) for more detailed video filter information 


*Last updated: 2025-07-09*


