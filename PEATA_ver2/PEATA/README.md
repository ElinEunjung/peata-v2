## Query Design Best Practices

When filtering videos by `keyword`, it is strongly recommended to combine it with either a `username` or a specific `region_code`.  
Otherwise, the TikTok Research API may return an `invalid_params` error, especially if the query is too broad.

| Condition | Result |
|:---|:---|
| `region_code` + `keyword` (rare keyword, small region) | Likely success |
| `region_code` + `keyword` (common keyword, large region) | May fail (invalid_params) |
| `username` + `keyword` | Highest chance of success |
| `keyword` only | Almost always fails |

**Best practice:** Always include a `username` when using `keyword` filters to ensure a successful query.

