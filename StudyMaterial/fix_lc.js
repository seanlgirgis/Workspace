const fs = require('fs');
const files_to_fix = [
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day1\\lc-0001-two-sum.ipynb",
        "pattern": "Hash Map (One-Pass)",
        "desc": "Storing complements in a hash map for O(1) lookups during iteration.",
        "use1": "Finding pairs that match a target condition.",
        "use2": "O(1) temporal lookups of previously seen streaming states.",
        "anti": "Need continuous ranges or sub-arrays (Use Sliding Window instead).",
        "b_time": "O(N^2)", "b_space": "O(1)",
        "o_time": "O(N)", "o_space": "O(N)"
    },
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day1\\lc-0217-contains-duplicate.ipynb",
        "pattern": "Hash Set",
        "desc": "Tracking uniqueness by inserting elements into a constant-time lookup set.",
        "use1": "Quick deduplication of streaming data.",
        "use2": "Detecting cyclical patterns or repeated states.",
        "anti": "Need to count exact frequencies (Use Hash Map instead).",
        "b_time": "O(N^2)", "b_space": "O(1)",
        "o_time": "O(N)", "o_space": "O(N)"
    },
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day1\\lc-0238-product-array-except-self.ipynb",
        "pattern": "Prefix / Suffix Arrays",
        "desc": "Pre-computing cumulative products from both directions to avoid division.",
        "use1": "Range queries where state depends on everything 'before' and 'after'.",
        "use2": "Avoiding division by zero operations in aggregate metrics.",
        "anti": "Queries that only look sequentially in one direction.",
        "b_time": "O(N^2)", "b_space": "O(1)",
        "o_time": "O(N)", "o_space": "O(1) auxiliary"
    },
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day1\\lc-0242-valid-anagram.ipynb",
        "pattern": "Frequency Counter",
        "desc": "Using an array or map to exact-match character counts between two sequences.",
        "use1": "Checking permutations or identical letter compositions.",
        "use2": "Fast distribution equality checks.",
        "anti": "Sequences where order matters (Use direct string comparison).",
        "b_time": "O(N \\log N)", "b_space": "O(1)",
        "o_time": "O(N)", "o_space": "O(1)"
    },
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day1\\lc-0347-top-k-frequent-elements.ipynb",
        "pattern": "Min-Heap / Bucket Sort",
        "desc": "Prioritizing top bounded elements without fully sorting the array.",
        "use1": "Leaderboards or 'Trending' items.",
        "use2": "Extracting highest-value events from logs dynamically.",
        "anti": "Need exact global median or strict sequential order of all N items.",
        "b_time": "O(N \\log N)", "b_space": "O(N)",
        "o_time": "O(N \\log K)", "o_space": "O(N)"
    },
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day2\\lc-0003-longest-substring-without-repeating-characters.ipynb",
        "pattern": "Sliding Window",
        "desc": "Expanding a right pointer and contracting a left pointer to bypass invalid states.",
        "use1": "Finding longest contiguous sequence meeting conditions.",
        "use2": "Deduplication applied to order-dependent streaming packets.",
        "anti": "Problem requires non-contiguous elements (Use subsequences/DP).",
        "b_time": "O(N^3)", "b_space": "O(min(N, M))",
        "o_time": "O(N)", "o_space": "O(min(N, M))"
    },
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day2\\lc-0076-minimum-window-substring.ipynb",
        "pattern": "Hard Sliding Window",
        "desc": "Tracking a variable `have` vs `need` state to dynamically expand and aggressively shrink.",
        "use1": "Extracting tightest valid sequences containing required keywords in logs.",
        "use2": "Satisfying complex subset requirements in a continuous data stream.",
        "anti": "Only looking for exact contiguous match of the entire subset exactly.",
        "b_time": "O(N^3)", "b_space": "O(S + T)",
        "o_time": "O(S + T)", "o_space": "O(S + T)"
    },
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day2\\lc-0121-best-time-to-buy-and-sell-stock.ipynb",
        "pattern": "State Tracking / Array",
        "desc": "Keeping track of the absolute minimum seen historically during a forward pass.",
        "use1": "Finding max single-pass deltas (swings) in time-series data.",
        "use2": "High Watermark / Low Watermark trailing gap analysis.",
        "anti": "Performing multiple transactions (Requires DP / State Machines).",
        "b_time": "O(N^2)", "b_space": "O(1)",
        "o_time": "O(N)", "o_space": "O(1)"
    },
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day2\\lc-0239-sliding-window-maximum.ipynb",
        "pattern": "Monotonic Deque",
        "desc": "Eliminating smaller historic values from a list since incoming larger values make them functionally useless.",
        "use1": "Real-time rolling max/min filters (e.g. trading volume spikes).",
        "use2": "Bounded expiration queues prioritizing magnitude over arrival time.",
        "anti": "Needing to track the median (Requires Two Heaps instead).",
        "b_time": "O(N \\times K)", "b_space": "O(N-K)",
        "o_time": "O(N)", "o_space": "O(K)"
    },
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day2\\lc-0424-longest-repeating-character-replacement.ipynb",
        "pattern": "Sliding Window & Dynamic Frequencies",
        "desc": "Validating a window using `size - max_freq <= k`.",
        "use1": "Error tolerance spans in noisy telemetry feeds.",
        "use2": "Contiguous streak analysis with allowed error fuzzing.",
        "anti": "Order of replacements matters for multiple characters.",
        "b_time": "O(N^3)", "b_space": "O(N)",
        "o_time": "O(N)", "o_space": "O(1)"
    },
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day3\\lc-0020-valid-parentheses.ipynb",
        "pattern": "Stack (LIFO)",
        "desc": "Pushing openers onto a stack and ensuring closers match the popped top.",
        "use1": "Inner-to-outer paired validation (JSON, HTML parsing).",
        "use2": "Preventing malformed hierarchical commands from hitting the database.",
        "anti": "Validating purely sequential states (State Machine is better).",
        "b_time": "O(N^2)", "b_space": "O(N)",
        "o_time": "O(N)", "o_space": "O(N)"
    },
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day3\\lc-0022-generate-parentheses.ipynb",
        "pattern": "Backtracking",
        "desc": "Decision-tree branching that instantly aborts paths breaking condition logic.",
        "use1": "Generating complex, strictly well-formed permutations for testing.",
        "use2": "Exploring localized state spaces with rigid correctness constraints.",
        "anti": "Simple combinatorial generation where all permutations are equally valid.",
        "b_time": "O(2^{2n} \\times n)", "b_space": "O(2^{2n})",
        "o_time": "O(4^n / \\sqrt{n})", "o_space": "O(N)"
    },
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day3\\lc-0150-evaluate-reverse-polish-notation.ipynb",
        "pattern": "Stack Evaluation",
        "desc": "Math evaluation left-to-right holding numbers until an operator triggers the top two.",
        "use1": "Fast algebraic interpreters without AST memory overhead.",
        "use2": "Safe evaluation of dynamic user-provided formulas.",
        "anti": "Nested, parenthesis-heavy algebraic equations (Requires shunting-yard).",
        "b_time": "O(N^2)", "b_space": "O(N)",
        "o_time": "O(N)", "o_space": "O(N)"
    },
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day3\\lc-0739-daily-temperatures.ipynb",
        "pattern": "Monotonic Stack",
        "desc": "Storing unresolved items (indices) in a stack until a resolving condition (larger value) arrives.",
        "use1": "Next Greater Element (NGE) algorithmic matching.",
        "use2": "Identifying time-to-recovery / rebound latency in market feeds.",
        "anti": "Simply finding the global historical maximum.",
        "b_time": "O(N^2)", "b_space": "O(1)",
        "o_time": "O(N)", "o_space": "O(N)"
    },
    {
        "path": "D:\\Workspace\\StudyMaterial\\Day3\\lc-0853-car-fleet.ipynb",
        "pattern": "Monotonic Stack (Sorting + Math)",
        "desc": "Traversing ordered data dynamically resolving collisions based on theoretical arrival limits.",
        "use1": "Time-distance collision detections (Batch congestion).",
        "use2": "Evaluating cascading system bottlenecks in pipeline processing.",
        "anti": "Two-dimensional vector intersection paths (Requires strict Euclidean math).",
        "b_time": "O(target \\times N)", "b_space": "O(N)",
        "o_time": "O(N \\log N)", "o_space": "O(N)"
    }
];

function generateSummary(item) {
    return [
        "## \ud83c\udfaf Summary: Key Takeaways\n",
        "\n",
        "### The Pattern\n",
        `**${item.pattern}** \u2014 ${item.desc}\n`,
        "\n",
        "### When to Use It\n",
        `- \u2705 ${item.use1}\n`,
        `- \u2705 ${item.use2}\n`,
        `- \u274c **Don't use when:** ${item.anti}\n`,
        "\n",
        "### Complexity\n",
        "| Approach | Time | Space |\n",
        "|----------|------|-------|\n",
        `| Brute Force | $${item.b_time}$ | $${item.b_space}$ |\n`,
        `| Optimal | $${item.o_time}$ | $${item.o_space}$ |\n`,
        "\n",
        "### Interview Confidence Checklist\n",
        "- [ ] Can explain the brute force and why it fails\n",
        "- [ ] Can state the pattern name and core insight in one sentence\n",
        "- [ ] Can write the optimal solution from memory\n",
        "- [ ] Can state time and space complexity with justification\n",
        "- [ ] Can name at least one real-world / Citi application"
    ];
}

function generateClosing(item) {
    return [
        "---\n",
        "\n",
        "**\"Simplicity and clarity is Gold.\"** \u2014 Sean's Study Mantra\n",
        "\n",
        `Master **${item.pattern}** and you've mastered one of the most common patterns in data engineering interviews. \ud83d\ude80`
    ];
}

for (let item of files_to_fix) {
    if (!fs.existsSync(item.path)) {
        console.log("FileNotFound: " + item.path);
        continue;
    }
    let nb = JSON.parse(fs.readFileSync(item.path, 'utf8'));

    // Check if it already has the closing mantra
    const lastCell = nb.cells[nb.cells.length - 1];
    if (lastCell.source.join('').includes("Sean's Study Mantra")) {
        console.log("Already processed " + item.path);
        continue;
    }

    nb.cells.push({
        "cell_type": "markdown",
        "id": "cell-summary-" + Math.random().toString(36).substr(2, 6),
        "metadata": {},
        "source": generateSummary(item)
    });

    nb.cells.push({
        "cell_type": "markdown",
        "id": "cell-closing-" + Math.random().toString(36).substr(2, 6),
        "metadata": {},
        "source": generateClosing(item)
    });

    fs.writeFileSync(item.path, JSON.stringify(nb, null, 1));
    console.log("Updated " + item.path + " - Cells: " + nb.cells.length);
}
