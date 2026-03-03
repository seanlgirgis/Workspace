---
created: 2026-03-02
updated: 2026-03-02
summary: Day 55 — String DP review, Snowflake + Databricks SQL comparison drill, and LinkedIn/network expansion.
tags: [study-plan, day-55, week-8, string-dp, snowflake-databricks, networking]
---

# Day 55 — String DP Review + Platform SQL Comparison + Networking

**Theme:** Your network is a parallel job search channel. Today you expand it deliberately.

---

## Daily Maintenance (35 min)

**LC — String DP (2 problems, timed):**
- LC #5 Longest Palindromic Substring (10 min — expand around center, both odd and even)
- LC #647 Palindromic Substrings (8 min — count version of LC #5)

After #5: explain why you need to expand for both odd-length (center at i) and even-length (center between i and i+1).

**SQL — Platform Comparison Drill:**

Write each query in both Snowflake syntax and standard SQL:
```sql
-- 1. Time travel: get yesterday's data
--    Snowflake: AT (OFFSET => -86400)
--    DuckDB/Standard: filter on report_date

-- 2. Upsert (MERGE)
--    Snowflake: MERGE INTO ... USING ... ON ... WHEN MATCHED THEN UPDATE ...
--    Delta Lake: MERGE INTO (same, but runs on Spark/Databricks)
--    PostgreSQL: ON CONFLICT DO UPDATE

-- 3. Array/JSON handling
--    Snowflake: ARRAY_CONTAINS, PARSE_JSON, FLATTEN
--    DuckDB: array_contains, json_extract, UNNEST
--    BigQuery: UNNEST, JSON_EXTRACT_SCALAR
```

Knowing the syntax variation across platforms signals genuine experience.

---

## Networking Expansion (40 min)

### LinkedIn — Active Search

Search for: "Senior Data Engineer [CITY]" + filter by 1st and 2nd connections.
Find 5 people you'd like to connect with who are:
- DEs at your target firms
- Hiring managers in DE at target firms
- Recruiters who specialize in DE at finance firms

Send each a connection request with a short note:
> "Hi [Name], I came across your profile while exploring Senior DE opportunities in [CITY]. I've been working in [APM / capacity planning / data engineering] for [X] years and would love to connect. Happy to chat if you have time."

Do NOT ask for a job or referral in the first message. Just connect.

### Warm Contact Follow-Up

For anyone who connected with you in Week 5 (Day 29 outreach) and hasn't responded:
- One more message: "Following up briefly — still interested in connecting if you have time."
- If still no response after this: move on. No third follow-up.

### Coffee Chat Requests

If someone responds positively, book a 20-minute call. Use this agenda:
1. Their role / what they work on (5 min)
2. What you're looking for and your background (5 min)
3. "What does [COMPANY]'s DE team value most in senior candidates?" (5 min)
4. "Are there any open roles I should look at or anyone else you'd recommend connecting with?" (5 min)

---

## Day 55 Checklist

- [ ] LC #5 palindrome — expand around center for both odd and even
- [ ] LC #647 counted correctly
- [ ] Platform SQL comparison written — Snowflake, DuckDB, Delta Lake syntax for all 3 patterns
- [ ] 5 LinkedIn connection requests sent with personalized notes
- [ ] Warm contacts from Day 29 followed up
- [ ] Coffee chat booked (or a slot offered) for any warm responses
