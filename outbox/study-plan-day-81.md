---
created: 2026-03-02
updated: 2026-03-02
summary: Day 81 — Network maintenance. Staying connected to the market and your professional community during and after the transition.
tags: [study-plan, day-81, week-12, networking, professional-network, career-maintenance]
---

# Day 81 — Network Maintenance

**Theme:** Your network got you here. Don't disappear when you don't need it. The relationships you maintain now are the ones that surface your next opportunity — or help you succeed in this one.

---

## Daily Maintenance (25 min)

**LC — Sliding Window (2 problems, timed):**
- LC #3 Longest Substring Without Repeating Characters (6 min — char → last index map; `start = max(start, last_seen[c] + 1)`)
- LC #424 Longest Repeating Character Replacement (8 min — window with max_freq; expand if `k >= window_size - max_freq`, else `start++`)

**SQL — Data quality check from memory:**
Write 4 Great-Expectations-style SQL checks for a table `daily_metrics(server_id, report_date, avg_cpu)`:
1. No nulls in server_id
2. avg_cpu between 0 and 100
3. Uniqueness on (server_id, report_date)
4. Row count for yesterday >= 1000

---

## Network Maintenance Session (50 min)

### Why Engineers Stop Networking

After landing a job, most engineers:
1. Stop checking LinkedIn
2. Stop attending meetups
3. Let relationships go cold

Then, 2 years later, they start a new search from zero — reaching out to people they haven't spoken to in years, who are suddenly receiving a "let's connect" message that clearly has an agenda.

The professionals who navigate careers well do the opposite: they stay connected when they don't need anything.

---

### The 4 Relationships to Maintain

**1. Your former colleagues**

The people you worked with for years are the most valuable professional relationships you have. They know your actual work quality — not your interview performance.

Action: In the first month after starting your new job, send a short message to 5-10 former colleagues you genuinely respected:
> "I started at [Company] last week — excited about the new challenge. I've really valued working with you and wanted to stay in touch. Would love to grab coffee sometime and hear what you're working on."

No ask. Just maintenance.

**2. Your recruiters**

The recruiters who ran your search process are a window into the market. Even after accepting, maintain the relationship:
> "I wanted to let you know I accepted an offer at [Company]. Thank you for the time you invested in this process. I've had a great experience working with you, and I'll certainly be in touch for future searches."

**3. Your interview contacts**

The engineers and managers who interviewed you — especially at companies where you went deep but didn't get the offer — respected you enough to give you their time. Stay connected.

For final round rejections at companies you respected: connect on LinkedIn with a note: "I really enjoyed our conversations. I hope our paths cross again." No bitterness, no explanation.

**4. The broader community**

Meetups, Slack communities, conference attendees. This is the long game — not transactional. Show up when you don't need anything. Comment thoughtfully on posts. Answer questions in DE Slack channels.

The person who helps others in a community is the one people reach out to when they have an opportunity.

---

### The Monthly 15-Minute Network Habit

Once a month, spend 15 minutes on network maintenance:

1. Scan your LinkedIn connections — who hasn't heard from you in 3+ months but matters?
2. Send 2-3 short, genuine messages: "Saw your post about X — interesting angle." "Heard [company] just shipped Y — congrats."
3. Reshare one piece of content that's genuinely useful to the people in your network. Don't spam, but don't disappear either.

**One rule:** never send a message that has an implicit ask hidden inside it. Pure generosity — or nothing.

---

### Building Your Personal Brand in the New Role

You've built real expertise: APM, streaming, finance data, system design. Now is the moment to start making it externally visible, while it's fresh.

Options (pick one, do it consistently):
- LinkedIn post: once a month, share one insight from what you're building or learning
- Blog post: 4/year is enough to establish presence
- Meetup talk: propose something short (10-15 min) at a local DE/data meetup
- Open source contribution: a small PR to a tool you actually use is more credible than a demo project

**The minimum viable personal brand:** a LinkedIn profile that makes someone reading it in 2027 immediately understand your expertise, and 3-4 posts in the last year that show you're active and thoughtful.

---

## Day 81 Checklist

- [ ] Both LC problems solved (Longest Repeating: max_freq + window size trick)
- [ ] 4 data quality SQL checks written from memory
- [ ] 5 former colleagues identified for "stay in touch" outreach
- [ ] Recruiter thank-you message drafted (or sent if already accepted)
- [ ] Monthly 15-minute network habit scheduled (calendar reminder)
- [ ] Personal brand choice made: LinkedIn / blog / meetup / open source — pick one
