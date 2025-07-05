# 🧼 Query Design Best Practices for PEATA TikTok API - Video

This guide summarizes best practices for building efficient, effective queries using TikTok’s Research API (Video), as tested and validated in the PEATA project.

> 🔗 Full test details are available in [query-test-log.md](./query-test-log.md)

---

## ✅ General Principles

* **Start date - End date** is must have parameter
* **Start simple**: Always begin with 1 or 2 filters and check the size/performance.
* **Respect the 30-day limit**: API rejects date ranges longer than 30 days.
* **Field selection matters**: Only include fields needed for analysis to speed up response.
* **Field deselection hides values** in response but columns still exist *(null-filled)* - need to be fixed.
* **Use `Add` button wisely**: In GUI, always click `Add` after changing filter values for `region_code` and `video_length`.

---

## ⚙️ Field-Specific Tips

### `video_id (Experimental)
- not tested yet

### `keyword`

* Works alone, returns results
* Use for simple topical queries
* comma-separated multiple value increace data (Need to change operation to IN from Equals)
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


### `music_id` / `effect_id` (Experimental)

* Often return sparse results — useful for trend backtracking
* Good to test with popular values + short date range

### `create_time` (Experimental)

* Supports `EQ`, `GT`, `LT`, `GTE`, `LTE`
* Use `GT`, `LT` for fine-grained time slicing (Experimental)

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

## 📊 When to Paginate

* If partial results returned, use `cursor` + `search_id` to continue (Experimental)
* Default max per page: 100 (but may return less)

---

## 📁 Field Set Strategy

* Use minimum field set for performance (e.g., `username`, `video_duration`)
* Avoid selecting `hashtag_info_list`, `effect_info_list`, etc., unless needed

---

*Last updated: 2025-07-05*


