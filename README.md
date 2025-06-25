## Query Design Best Practices  <-- NEED TO BE TESTED AGAIN

When filtering videos by `keyword`, it is strongly recommended to combine it with either a `username` or a specific `region_code`. 
Otherwise, the TikTok Research API may return an `invalid_params` error, especially if the query is too broad.

| Condition | Result |
|:---|:---|
| `region_code` + `keyword` (rare keyword, small region) |  |
| `region_code` + `keyword` (common keyword, large region) |  |
| `username` + `keyword` |  |
| `keyword` only |  |

**Best practice:** Always start with broad search with single filter. Normally, multiple `keyword` ensures a successful query.

