# 🧪 PEATA Query Test Log

This document summarizes the query tests conducted for the PEATA application using TikTok’s Research API (Video). It helps refine the guidance in the "Query Design Best Practices" document and verify implementation.

> 📘 See best-practices summary in [query-best-practices.md](./query-best-practices.md)

---

## ✅ General Observations

* `keyword` alone works well to retrieve results
* ❌ Date ranges exceeding 30 days return `invalid_params` error
* ✅ `region_code` and `video_length` can be added using the **Add** button
* ⚠️ When modifying a filter in operation (IN or Equals), value in `region_code`, users must **click Add again** to update the query. Always verify the Live Query Preview to ensure it reflects the update.
* ✅ Multiple `region_code` values can be entered as comma-separated
* ✅ Start/End Date inputs can be edited by typing directly
* ✅ If a field is **unchecked**, returned data excludes its values but **columns still appear** in the dataset
* ⚠️ Use the Max Result Option (100 / 500 / 1000 / ALL) wisely. Selecting **ALL** often leads to API failure after long processing time. However, partial data is usually available for download.
* ⚠️ All current tests were performed using ALL option. Most resulted in API failure during download. Lower result limits tend to succeed more reliably.

---

## 📊 PEATA Query Test Table
| Query Conditions                            | Exclusion             | Logic          | Date Range           | Max | Server | Result         | Time    |
|--------------------------------------------|------------------------|----------------|-----------------------|------|--------|----------------|---------|
| `username: billboard`                         | –                      | AND            | 20250604 - 20250704   | ALL  | ✅      | 220 items       | 4s      |
| `username: houseofhighlights`                 | –                      | AND            | 20250605 - 20250705   | ALL  | ✅      | 1326 items      | 33s     |
| `keyword: bts`                                 | –                      | AND            | 20250604 - 20250704   | ALL  | ❌      | 3658 items      | 1m44s   |
| `keyword: bts`                                 | –                      | AND            | 20250604 - 20250604   | ALL  | ❌      | 14766 items     | ⚠️ 7m32s |
| `music_id: 7423463770629520000`               | –                      | AND            | 20250605 - 20250705   | ALL  | ✅      | no data         | –       |
| `region_code: NO`, `keyword: fjord`             | –                      | AND            | 20250604 - 20250704   | ALL  | ✅      | 1803 items      | –       |
| `region_code: US`, `keyword: dance`             | –                      | AND            | 20250604 - 20250704   | ALL  | ❌      | 4209 items      | 2m20s   |
| `region_code: US`, `keyword: dance`             | –                      | AND            | 20250604 - 20250604   | ALL  | ❌      | 3789 items      | 1m46s   |
| `region_code: US`, `hashtag: funny`             | –                      | AND            | 20250605 - 20250705   | ALL  | ❌      | 29518 items     | ⚠️ 11m27s |
| `region_code: US, GB`, `keyword: education`     | –                      | AND            | 20250604 - 20250604   | ALL  | ❌      | 12121 items     | ⚠️ 5m53s |
| `video_length: LONG, EXTRA_LONG`              | –                      | OR             | 20250604 - 20250704   | ALL  | ❌      | 11054 items     | 3m35s   |
| `video_length: LONG, EXTRA_LONG`              | –                      | OR             | 20250604 - 20250604   | ALL  | ❌      | 24376 items     | ⚠️ 6m    |
| `region: US, GB` + `keyword: education`         | NOT: `hashtag: funny`    | AND + OR + NOT | 20250605 - 20250705   | ALL  | ❌      | 9217 items      | 3m44s   |
| `region_code: US`, `keyword: food`              | NOT: `hashtag: mukbang`  | AND + NOT      | 20250605 - 20250705   | ALL  | ❌      | 5342 items      | 2m17s   |

---

## ⏳ Planned Test (Next Round)

Suggested test queries for next round:

### 🎵 `music_id` :

* `music_id: 7416431989534840000` + `region_code: US` + `date: 20250605-20250705`
* `music_id: 7423463770629520000` + `date: 20250605 only`

### 🔬 `effect_id` :

* `effect_id: 1234567890123456789` + `date: 20250605 only`
* `effect_id` + `region_code: IN, US` + keyword: fashion + `date: 20250604 only`

### 🔬 `create_time` logic tests:

* Use operation: `GT`, `LT`, `GTE`, `LTE` with `create_date`
* Examples:

  * `create_date > 20250601` AND keyword: news
  * `create_date < 20250610` AND hashtag: health

---

*Last updated: 2025-07-05*
