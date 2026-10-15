# Figure: why --cpus 6 might help when --cpus 24 didn't

What it should show: final assembly merges 256 shards with an internal concurrency window `W = clamp(threads, 1, 8)`. At any instant, W shards are being actively decoded and merged into the output, each holding its own transient working buffer (decoded k-mer/row pool for that shard) in memory on top of whatever's already been merged into the resident output so far.

Two side-by-side bar stacks, same card style as the other figures:

**Left bar, "attempts 1-3, --cpus 24."** `clamp(24, 1, 8)` still clamps to 8, so all three failed attempts actually ran with W=8 the whole time, no matter how much total memory was requested. Draw a tall base block ("already-merged output, grows over the run") with 8 small blocks stacked beside it ("8 concurrent shard buffers"). A dashed red line marks the OOM ceiling, crossed by this stack.

**Right bar, "attempt 4, --cpus 6."** `clamp(6, 1, 8)` = 6 for the first time, actually lowering W below its usual ceiling. Same base block, but only 6 small blocks beside it. The dashed OOM line is the same height as the left bar, but this stack's peak sits under it.

Callout text under both: "The 1,500 -> 1,650 -> 1,800 GB increases across attempts 1-3 only raised the ceiling. None of them touched W, which stayed pinned at 8 the whole time. --cpus 6 is the first attempt to actually shrink the number of shard buffers resident at once, rather than just giving the same 8 buffers more room."

Style: dark card (`#151f1b`), base block in dim gray-green, the W shard-buffer blocks in accent green (`#3ecfa2`), the OOM ceiling as a dashed warm red/orange line (`#e58468`).

Current attempt: `assembly_concurrency.svg` is hand-built, illustrative block heights only (the real per-shard transient footprint isn't independently measured, only the aggregate crash behavior is). The point is the shape of the argument (same ceiling, fewer concurrent buffers), not a quantitatively accurate memory breakdown.
