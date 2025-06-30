# 📘 PEATA App Usage Guide

## 🚀 Getting Started

1. **Launch** the app.
2. **Sign in** with valid TikTok Research API credentials.
3. **Choose a query type** from the left navigation menu:

   * Video Query
   * Comment Query
   * User Info Query

---

## 🎯 Setting Filters & Fields

### Video Query Tips

* All fields are checked by default.
* You may uncheck any fields not needed in the result.
* **Filter rows** support multiple inputs via comma-separated values:

  * Example: `food, recipe, cooking` for keyword field.
* Logical operations include:

  * `EQ`: exact match (e.g., `username EQ elin0615`)
  * `IN`: matches any in list (e.g., `username IN [elin0615, jxdn]`)
  * `GT`, `GTE`, `LT`, `LTE` for date and numeric fields

### Filter Logic Builder

* You can combine multiple filter conditions using:

  * **AND** (all conditions must be true)
  * **OR** (at least one condition is true)
  * **NOT** (none of the conditions are true)
* Each condition has:

  * `field_name`
  * `operation`
  * `field_values`

### Example Query (JSON format)

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

> 💡 Note: `end_date` cannot exceed `start_date + 30 days`.

---

## 📦 Running Queries

4. **Select Max Results** from dropdown (default: 500)

   * Over 1000 may exceed API quota.

5. **Click "Run Query"** to send the request.

   * On success, results are shown in a table.
   * Missing required filters (e.g. no date range) will trigger an error.

6. **Use "Load More"** to paginate results (Up to 100 rows per click).

   * Button disappears when all data is loaded.
   * For unsatisfactory data quality, click **“Back to Query”** to adjust your filters.

---

## 💾 Exporting Data

7. **Click Export** to download as `.csv` or `.xlsx`

   * A progress bar shows during export.
   * Large exports may appear *frozen* but are processing.
   > Don't worry if the app seems unresponsive during large exports — it's working! 😊
   * Messages confirm success/failure.

8. **Find exported files** in the `/data/` folder:

   * `csv/` for CSV exports
   * `excel/` for Excel exports

---

## 📚 Related Docs

* [TikTok Video Filter Guide](video-filter-guide.md) *(coming soon)*
* [Query Best Practice Tips](query-best-practices.md) *(coming soon)*
