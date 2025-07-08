# ЁЯзк PEATA Query Test Log

This document summarizes the query tests conducted for the PEATA application using TikTokтАЩs Research API (**Video**). It helps refine the guidance in the "Query Design Best Practices" document and verify implementation.

> ЁЯУШ See best-practices summary in [query-best-practices.md](./query-best-practices.md)

---

## тЬЕ General Observations

* `keyword` alone works well to retrieve results
* тЭМ Date ranges exceeding 30 days return `invalid_params` error
* тЬЕ `region_code` and `video_length` can be added using the **Add** button
* тЪая╕П When modifying a filter in operation (IN or Equals), value in `region_code`, users must **click Add again** to update the query. Always verify the Live Query Preview to ensure it reflects the update.
* тЬЕ Multiple `region_code` values can be entered as comma-separated
* тЬЕ Start/End Date inputs can be edited by typing directly
* тЬЕ If a field is **unchecked**, returned data excludes its values but **columns still appear** in the dataset
* тЪая╕П Use the Max Result Option (100 / 500 / 1000 / ALL) wisely. Selecting **ALL** often leads to API failure after long processing time. However, partial data is usually available for download.
* тЪая╕П All current tests were performed using ALL option. Most resulted in API failure during download. Lower result limits tend to succeed more reliably.

---

## ЁЯУК PEATA Query Test Table
| Query Conditions                            | Exclusion             | Logic          | Date Range           | Max | Server | Result         | Time    |
|--------------------------------------------|------------------------|----------------|-----------------------|------|--------|----------------|---------|
| `username: billboard`                         | тАУ                      | AND            | 20250604 - 20250704   | ALL  | тЬЕ      | 220 items       | 4s      |
| `username: houseofhighlights`                 | тАУ                      | AND            | 20250605 - 20250705   | ALL  | тЬЕ      | 1326 items      | 33s     |
| `keyword: bts`                                 | тАУ                      | AND            | 20250604 - 20250704   | ALL  | тЭМ      | 3658 items      | 1m44s   |
| `keyword: bts`                                 | тАУ                      | AND            | 20250604 - 20250604   | ALL  | тЭМ      | 14766 items     | тЪая╕П 7m32s |
| `music_id: 7423463770629520000`               | тАУ                      | AND            | 20250605 - 20250705   | ALL  | тЬЕ      | No data         | тАУ       |
| `region_code: NO`, `keyword: fjord`             | тАУ                      | AND            | 20250604 - 20250704   | ALL  | тЬЕ      | 1803 items      | тАУ       |
| `region_code: US`, `keyword: dance`             | тАУ                      | AND            | 20250604 - 20250704   | ALL  | тЭМ      | 4209 items      | 2m20s   |
| `region_code: US`, `keyword: dance`             | тАУ                      | AND            | 20250604 - 20250604   | ALL  | тЭМ      | 3789 items      | 1m46s   |
| `region_code: US`, `hashtag: funny`             | тАУ                      | AND            | 20250605 - 20250705   | ALL  | тЭМ      | 29518 items     | тЪая╕П 11m27s |
| `region_code: US, GB`, `keyword: education`     | тАУ                      | AND            | 20250604 - 20250604   | ALL  | тЭМ      | 12121 items     | тЪая╕П 5m53s |
| `video_length: LONG, EXTRA_LONG`              | тАУ                      | OR             | 20250604 - 20250704   | ALL  | тЭМ      | 11054 items     | 3m35s   |
| `video_length: LONG, EXTRA_LONG`              | тАУ                      | OR             | 20250604 - 20250604   | ALL  | тЭМ      | 24376 items     | тЪая╕П 6m    |
| `region: US, GB` + `keyword: education`         | NOT: `hashtag: funny`    | AND + OR + NOT | 20250605 - 20250705   | ALL  | тЭМ      | 9217 items      | 3m44s   |
| `region_code: US`, `keyword: food`              | NOT: `hashtag: mukbang`  | AND + NOT      | 20250605 - 20250705   | ALL  | тЭМ      | 5342 items      | 2m17s   |`music_id: 7416431989534840000` + `region_code: US` | - | AND | 20250608-20250708 | ALL | ✅ | No data | - |
|`music_id: 7416431989534840000` | - | AND | 20250608-20250708 | ALL | ✅ | No data | - |

---

## тП│ Planned Test (Next Round)

Suggested test queries for next round:

### ЁЯО╡ `music_id` :

* `music_id: 7416431989534840000` + `region_code: US` + `date: 20250605-20250705`
* `music_id: 7423463770629520000` + `date: 20250605 only`



### ЁЯФм `create_time` logic tests:

* Use operation: `GT`, `LT`, `GTE`, `LTE` with `create_date`
* Examples:

  * `create_date > 20250601` AND keyword: news
  * `create_date < 20250610` AND hashtag: health

---

*Last updated: 2025-07-05*
