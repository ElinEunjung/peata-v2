# 🎯 TikTok Video Filter Guide
This guide explains how to build advanced filters for querying TikTok video data using PEATA.

---

## ⚙️ Supported Fields & Operations

You can filter video data using the following fields:

| Field Name     | Type      | Allowed Operations       | Notes |
|----------------|-----------|--------------------------|-------|
| create_date    | date      | EQ, IN, GT, GTE, LT, LTE | Format: `YYYYMMDD` |
| username       | string    | EQ, IN                   | The username of the video creator (e.g., `cookie_love_122`) |
| region_code    | string    | EQ, IN                   | A two digit country code (e.g., `US`, `JP`) |
| video_id       | int64     | EQ, IN                   | Unique video ID (e.g., `6978662169214864645` |
| hashtag_name   | string    | EQ, IN                   | e.g., `arianagrande`, `celebrity` |
| keyword        | string    | EQ, IN                   | Searches in video description (e.g., `tiktok`)|
| music_id       | int64     | EQ, IN                   | ID of used music (e.g., `8978345345214861235` |
| effect_id      | int64     | EQ, IN                   | Video effect ID `3957392342148643476` |
| video_length   | string    | EQ, IN                   | `SHORT` (<15s), `MID` (15 ~60s), `LONG`(1~5min), `EXTRA_LONG`(>5min) |

---

## 🔁 Logic Operators

TikTok supports logic-based queries using combinations of:

- **AND**: All conditions must be satisfied
- **OR**: At least one condition must be satisfied
- **NOT**: Excludes results matching condition

Each condition has:

```json
{
  "operation": "EQ",
  "field_name": "username",
  "field_values": ["elin0615"]
}
```
---

## Explanation of EQ, IN, GT, etc.

| Condition Operation    | Type   | Explanation  |
|------------------------|--------|--------------|  
| EQ  | string, int, date | Equals (exact match) | 
| IN  | string, int    | IN (Matches any in list) |
| GT  | date    | Greater than |
| GTE | date    | Greater than or equal | 
| LT  | date    | Less than |
| LTE | date    | Less than or equal | 

- `Equals`: exact match (e.g., `username EQ elin0615`)
- `IN`: matches any in list (e.g., `username IN [elin0615, jxdn]`)
- `Greater than`, `Greater or equal`, `Less than`, `Less or equal` are only for `create_time` field.
- Always check Live Query Preview to check your query is correctly formed **Run Query**

---

## 📌 Filtering Tips

- Comma-separated values supported
- Use **IN** for multiple values:  
  `region_code IN ["US", "JP"]`
- `start_date` and `end_date` are top-level keys, not part of the filter
   * `end_date` must be ≤ 30 days after `start_date`
- Keyword matches only video descriptions, not hashtags or comments
- `region_code` can be chosen by scrolling dropdown menu or by typing directly. 
   * Multiple region typing(comma-separated) is possible
   * Always click **Add** button after typing.
   * Example: `US, JP` + **Add** 
>  For multiple value, **ALWAYS** make sure logical operator is set to `IN`, otherwise it will return "invalid query parameters" error.

---

## Region codes

Tiktok supports two digit country code below :

'FR', 'TH', 'MM', 'BD', 'IT', 'NP', 'IQ', 'BR', 'US', 'KW', 'VN', 'AR', 'KZ', 'GB', 'UA', 'TR', 'ID', 'PK', 'NG', 'KH', 'PH', 'EG', 'QA', 'MY', 'ES', 'JO', 'MA', 'SA', 'TW', 'AF', 'EC', 'MX', 'BW', 'JP', 'LT', 'TN', 'RO', 'LY', 'IL', 'DZ', 'CG', 'GH', 'DE', 'BJ', 'SN', 'SK', 'BY', 'NL', 'LA', 'BE', 'DO', 'TZ', 'LK', 'NI', 'LB', 'IE', 'RS', 'HU', 'PT', 'GP', 'CM', 'HN', 'FI', 'GA', 'BN', 'SG', 'BO', 'GM', 'BG', 'SD', 'TT', 'OM', 'FO', 'MZ', 'ML', 'UG', 'RE', 'PY', 'GT', 'CI', 'SR', 'AO', 'AZ', 'LR', 'CD', 'HR', 'SV', 'MV', 'GY', 'BH', 'TG', 'SL', 'MK', 'KE', 'MT', 'MG', 'MR', 'PA', 'IS', 'LU', 'HT', 'TM', 'ZM', 'CR', 'NO', 'AL', 'ET', 'GW', 'AU', 'KR', 'UY', 'JM', 'DK', 'AE', 'MD', 'SE', 'MU', 'SO', 'CO', 'AT', 'GR', 'UZ', 'CL', 'GE', 'PL', 'CA', 'CZ', 'ZA', 'AI', 'VE', 'KG', 'PE', 'CH', 'LV', 'PR', 'NZ', 'TL', 'BT', 'MN', 'FJ', 'SZ', 'VU', 'BF', 'TJ', 'BA', 'AM', 'TD', 'SI', 'CY', 'MW', 'EE', 'XK', 'ME', 'KY', 'YE', 'LS', 'ZW', 'MC', 'GN', 'BS', 'PF', 'NA', 'VI', 'BB', 'BZ', 'CW', 'PS', 'FM', 'PG', 'BI', 'AD', 'TV', 'GL', 'KM', 'AW', 'TC', 'CV', 'MO', 'VC', 'NE', 'WS', 'MP', 'DJ', 'RW', 'AG', 'GI', 'GQ', 'AS', 'AX', 'TO', 'KN', 'LC', 'NC', 'LI', 'SS', 'IR', 'SY', 'IM', 'SC', 'VG', 'SB', 'DM', 'KI', 'UM', 'SX', 'GD', 'MH', 'BQ', 'YT', 'ST', 'CF', 'BM', 'SM', 'PW', 'GU', 'HK', 'IN', 'CK', 'AQ', 'WF', 'JE', 'MQ', 'CN', 'GF', 'MS', 'GG', 'TK', 'FK', 'PM', 'NU', 'MF', 'ER', 'NF', 'VA', 'IO', 'SH', 'BL', 'CU', 'NR', 'TP', 'BV', 'EH', 'PN', 'TF', 'RU'

---

## 🧪 Example Query (JSON format in Live Query Preview)

```json
{
  "and": [
    { "operation": "EQ", "field_name": "username", "field_values": ["elin0615"] },
    { "operation": "IN", "field_name": "region_code", "field_values": ["US", "JP"] }
  ],
  "not": [
    { "operation": "LT", "field_name": "create_date", "field_values": ["20230101"] }
  ]
}
```
---

## 📎 Related

- [PEATA App Usage Guide](usage.md)
- [TikTok Research API Specs - Query Videos](https://developers.tiktok.com/doc/research-api-specs-query-videos)

