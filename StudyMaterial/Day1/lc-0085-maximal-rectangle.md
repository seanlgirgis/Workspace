---
created: 2026-02-27
updated: 2026-02-27
summary: LeetCode 85 - Maximal Rectangle. Using the DP Rolling Histogram and O(N) Monotonic Stack helper.
tags: [leetcode, hard, python, array, dynamic-programming, monotonic-stack, study]
workbench: D:\LeetCode\LC_0085.ipynb
---

# LeetCode 85: Maximal Rectangle

## The Core Concept
How does a 2D matrix of 1s and 0s relate to the 1D Histogram from LeetCode #84? 
If we look at the matrix row by row, building from the top down, **each row can be treated as the *base* of a histogram.**

---

## 5-Minute Interview Intuition

If you get this question, your thought process should be:
1. "Finding the maximal rectangle in a 2D matrix is actually just solving *Largest Rectangle in Histogram* $R$ consecutive times."
2. "I can reuse the $O(N)$ Monotonic Stack helper function from LC 84."
3. "To build the histograms efficiently, instead of counting downwards for every cell ($O(R^2 \times C)$), I will use a **Dynamic Programming Rolling Array**."

## The DP Rolling Array Optimization ($O(R \times C)$)
Instead of shooting a loop downwards to count `1`s for every single cell, iterate **Top-Down** exactly once.

Maintain a single 1D `histo` array. As you move down row by row:
1. If `matrix[r][c] == "1"`, the histogram bar grows: `histo[c] += 1`
2. If `matrix[r][c] == "0"`, the bar is cut off at the base!: `histo[c] = 0`

Pass this perfectly updated `histo` array into your $O(N)$ stack function after every row.

---

## The Optimized Solution
*Runnable notebook → workbench: `D:\LeetCode\LC_0085.ipynb`*

```python
def maximalRectangle_optimized(matrix):
    if not matrix or not matrix[0]: return 0
        
    # Standard O(N) stack helper from LC 84
    def largestRectangleArea(heights):
        max_area = 0
        stack = []
        for i, h in enumerate(heights):
            start = i
            while stack and stack[-1][1] > h:
                idx, val = stack.pop()
                max_area = max(max_area, val * (i - idx))
                start = idx
            stack.append((start, h))
        for i, h in stack:
            max_area = max(max_area, h * (len(heights) - i))
        return max_area

    max_max_area = 0
    cols = len(matrix[0])
    histo = [0] * cols
    
    # DP Rolling Histogram: Top-Down pass
    for row in matrix:
        for c in range(cols):
            if row[c] == "1":
                histo[c] += 1
            else:
                histo[c] = 0  # 0 cuts off any rectangle dropping from above
                
        # Analyze the fully updated histogram for this row
        max_max_area = max(max_max_area, largestRectangleArea(histo))
        
    return max_max_area
```
