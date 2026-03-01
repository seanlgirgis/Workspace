---
created: 2026-02-27
updated: 2026-02-27
summary: LeetCode 84 - Largest Rectangle in Histogram. Intuition, Monotonic Stack Optimization, and Time Complexity Proof.
tags: [leetcode, hard, python, array, monotonic-stack, study]
workbench: D:\LeetCode\LC_0084.ipynb
---

# LeetCode 84: Largest Rectangle in Histogram

## The Core Insight
For any bar, the largest rectangle using its **full height** is decided by how far left and right you can stretch until you hit a bar *shorter* than the current one.

---

## The $O(N)$ Optimization: The Monotonic Stack
Instead of doing $O(N^2)$ work by walking backwards manually for every single bar, we use a **Stack** as a "waiting room".

1. If a bar is taller than the one before it, it goes into the waiting room.
2. If we hit a bar that is **shorter** than the top of our stack, that short bar has officially **blocked** the rectangle of the taller bar from expanding any further right.
3. We `pop()` the taller bar out of the stack, calculate its final area immediately, and confidently update our `max_area`.

## The "Amortized" $O(N)$ Proof
*Interview talking point for when they ask about the inner `while` loop:*

> "It looks like $O(N^2)$ because of the nested `while` loop, but we must look at the lifecycle of a single bar. A bar can only be pushed onto the stack exactly once, and popped off exactly once. This means across the entire outer loop, the inner `while` loop can only execute a maximum of $N$ times total. The total operations are bounded by $2N$, which simplifies mathematically to an amortized $O(N)$ time complexity."

---

## The Optimized Solution
*Runnable notebook → workbench: `D:\LeetCode\LC_0084.ipynb`*

```python
def largestRectangleArea_optimized(heights):
    max_area = 0
    stack = []  # Will store pairs of (starting_index, height)

    for index, height in enumerate(heights):
        start = index

        # We hit a shorter bar! The waiting room is blocked.
        # Pop rectangles and finalize their area.
        while stack and stack[-1][1] > height:
            popped_index, popped_height = stack.pop()
            max_area = max(max_area, popped_height * (index - popped_index))
            # The new shorter bar can effectively "reach back" to where the popped bar started
            start = popped_index

        stack.append((start, height))

    # Cleanup: Any bars left were never blocked on the right!
    for index, height in stack:
        max_area = max(max_area, height * (len(heights) - index))

    return max_area
```
