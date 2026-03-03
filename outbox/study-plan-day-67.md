---
created: 2026-03-02
updated: 2026-03-02
summary: Day 67 — Technical presentation skills. Whiteboard design, verbal walkthroughs, and communicating to mixed audiences.
tags: [study-plan, day-67, week-10, presentation, whiteboard, communication, final-round]
---

# Day 67 — Technical Presentation Skills

**Theme:** In a final round, you're often presenting to a mixed audience — some technical, some not. Your ability to shift register mid-presentation is what separates senior candidates.

---

## Daily Maintenance (25 min)

**LC — Graph BFS (2 problems, timed):**
- LC #994 Rotting Oranges (8 min — multi-source BFS, count fresh at start, decrement on spread)
- LC #1091 Shortest Path in Binary Matrix (8 min — BFS with 8-directional neighbors, return steps)

**SQL — Recursive CTE from memory:**
Write the manager hierarchy query: given `employees(id, name, manager_id)`, list all reports under a given manager at any depth. Include depth column.

---

## Technical Presentation Session (60 min)

### Why Presentation Is a Technical Skill

Final rounds often include:
- A system design you draw on a whiteboard while narrating
- A "walk us through your approach" for a past project
- A panel with both engineers and business stakeholders

The failure mode: candidate designs correctly but narrates poorly. The panel doesn't know what to look at. Questions come in from all directions. The candidate loses the thread.

---

### The 4-Layer Communication Stack

When presenting technical content to a mixed audience, layer your message:

| Layer | Audience | What to say |
|-------|----------|-------------|
| Business context | Everyone | "The problem we're solving is..." |
| System overview | Everyone | "At the highest level, data flows like this..." |
| Key decisions | Technical | "We chose Kafka here because..." |
| Trade-offs | Technical | "The alternative would have been..." |

Lead with business context. Drop to technical depth when technical people probe. Return to business language when non-technical people are in the room.

---

### Whiteboard Design Protocol

When drawing a system design on a whiteboard:

**Step 1 — Anchor with requirements (2 min)**
Say: "Before I draw anything, let me confirm what we're optimizing for."
Write 3 bullets on the board: scale, latency target, consistency requirement.

**Step 2 — Draw the data path, not the components (start here)**
Don't draw boxes first. Draw the data flow:
`Source → [??] → [??] → [??] → Consumer`
Fill in the boxes as you narrate why each one is there.

**Step 3 — Narrate every line you draw**
Never draw in silence. "This arrow from Kafka to Flink represents the stream ingestion — it's asynchronous here because we want the producer to be decoupled from processing latency."

**Step 4 — Annotate with numbers**
Write scale numbers next to components: "~50K events/sec here," "P99 < 200ms here," "7-year retention on this path."

**Step 5 — Leave space for probes**
After drawing, say: "There are a few places where I made deliberate choices I'd love to walk through if it's useful — the storage layer and the failure handling."

---

### Practice: The 8-Minute Design Narration

Set a timer for 8 minutes. Narrate out loud (no audience needed) a design for:

**Prompt:** "Walk me through how you'd build a daily report that tells trading managers whether their desks are at risk of breaching regulatory capital limits."

Your narration must hit:
1. What problem are we solving? (business frame, 30 sec)
2. What data do we need and where does it come from? (1 min)
3. How does it get processed? (2 min — pipeline)
4. How does the output reach the right people? (1 min — alerting, dashboard)
5. What's the biggest risk in this design? (1 min)
6. How would you know it's working? (30 sec — monitoring, SLA)

After: score yourself. Did you finish in 8 minutes? Did you mention the business frame? Did you explicitly name a risk?

---

### Adjusting for a Non-Technical Stakeholder in the Room

When a VP, product manager, or business analyst is in the room during your technical presentation:

- **Swap every tool name for a capability description.** Not "Kafka" — "a message queue that lets systems communicate without being tightly coupled." Not "Delta Lake" — "a storage layer that gives us the ability to correct data after the fact."
- **Check in every 2 minutes.** "Does that make sense at the level I'm describing, or would it help to go deeper on any part?"
- **Frame trade-offs in business terms.** Not "this is O(n log n)" — "this approach gets slower as data volume grows, so we'd need to revisit if volume 10x'd."

---

## Day 67 Checklist

- [ ] Both LC problems solved (Rotting Oranges: count fresh first, decrement)
- [ ] Recursive CTE with depth column written from memory
- [ ] Read the 4-layer communication stack — understand which layer is for whom
- [ ] 8-minute design narration completed out loud (regulatory capital report)
- [ ] Score: finished in time ✓, business frame ✓, named a risk ✓
- [ ] Practice translating one tool name into a capability description for a non-technical audience
