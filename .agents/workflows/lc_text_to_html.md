---
description: Convert LeetCode problem text into a fully styled HTML study guide card based on a reference template.
---

# LC-TEXT-TO-HTML (Skill)

**Trigger Statement:** `"lc html: [paste problem text] — folder: [Destination Folder Path]"`

**Instructions for the Agent:**
0. **Reference Constraint:** Before you generate any HTML, you MUST use the `view_file` tool to read `D:\Workspace\StudyMaterial\Day2\lc-0076-minimum-window.html`. Pay extremely close attention to its unique Parts, style structure and contents.

1. **Read Reference Template:**
   - Immediately use the `view_file` tool to read the contents of `D:\Workspace\StudyMaterial\Day8\lc-0104-max-depth.html`.
   - **DO NOT** use embedded CSS templates. Extract the CSS block and the exact HTML skeleton patterns directly from this reference file. This ensures you always use the latest styling.

2. **File Naming Convention:**
   - Parse the LeetCode number and title from the input text.
   - Generate a slugified filename format matching the reference: `lc-[4-digit-number]-[kebab-case-title].html` (e.g., `lc-0104-max-depth.html`).
   - The final output path will be `[Destination Folder Path]\[Generated Filename]`.

3. **Theme & CSS Mapping:**
   - Extract the CSS block from the reference file. The CSS will contain substitution slots like `[g1]`, `[g2]`, and `[accent]`.
   - Determine the Problem Category (e.g., Trees, Binary Search, Heap, Intervals, HashMap, Sliding Window, Stack, DP).
   - Apply the correct gradient/color theme based on the Category to the CSS slots.

4. **HTML Structure & Content Generation:**
   - Use the **exact HTML patterns** from the reference file for all 7 sections: main card, parameter table, insight box, code blocks, Q&A format, and the Citi Angle box.
   - **Do not invent new HTML structures.** Emit the exact HTML skeleton extracted from step 1, substituting the content with the provided problem text.
   
5. **Citi Angle Generation:**
   - You MUST generate a "Citi Angle" section mapping the algorithm to a plausible APM/FinTech scenario (e.g., transaction trees, system latency, risk intervals), even if the input text does not include one.

6. **Interview Q&A Expansion:**
   - The output MUST contain a **minimum of 5 Q&A pairs**.
   - If the user's pasted text contains fewer than 5 pairs, generate additional high-quality, relevant Q&A pairs related to time/space complexity, edge cases, or trade-offs to reach the minimum of 5.

7. **Closing Mantra:**
   - The exact string `"Simplicity and clarity is Gold." — Sean's Study Mantra 🚀` MUST appear at the very bottom of every generated file, styled as it is in the reference.

8. **Output Execution:**
   - Generate the final HTML document in memory.
   - Use the `write_to_file` tool to save the HTML content to the calculated destination path.
   - Inform the user of the successful creation and provide the file path.