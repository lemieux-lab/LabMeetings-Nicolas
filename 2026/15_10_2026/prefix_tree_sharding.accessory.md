# Figure: adaptive prefix-tree sharding

What it should show: a variable-depth tree, shallow everywhere the data is sparse, deeper only where a shard is genuinely dense. Not a balanced tree, that's the whole point.

**Top row: a sample of the 256 original shards (8-bit prefix).** Draw ~14 small boxes in a row, most green ("under target T, left completely untouched, no read, no write"), with an ellipsis implying the other ~230 untouched shards continue off to the sides, plus 2 boxes in orange ("over T, flagged for splitting"). Label the row "256 shards, 8-bit prefix, stat'd across all 5 roots (~26 flagged, ~230 untouched)".

**Case 1, a modest split (`shard37`).** One line down from the orange `shard37` box to 4 green leaf boxes labeled `shard37_0` .. `shard37_3`. One level of splitting (a couple more bits) was enough to get every child under T. Label this branch "+ a few bits, done".

**Case 2, the worst case (`shard82`, the ~41.8 GB max shard).** Lines down from the orange `shard82` box to 4 children. 3 of those are green leaves immediately. The 4th is still orange (still over T after one split) and itself splits again into 4 more green leaves one row deeper. Label the two split levels so it's visually obvious this branch went deeper than case 1, ending at `shard82_0` .. roughly `shard82_15` (the real count is "~14-16 children needed," not necessarily a clean power of 2, the figure's exact child count is illustrative).

**Bottom: a small manifest callout.** A little card or list showing a couple of example rows: `shard37.bin` (untouched, depth 8) and `shard82_3_2.bin` (recursively split, deeper). This is what assembly actually iterates over instead of a flat 0..255 range.

Style: match `double_strand_counting.svg` and `assembly_concurrency.svg`, dark card (`#151f1b`), green (`#3ecfa2`) for leaves/untouched shards, warm orange (`#e58468`) for flagged/still-splitting shards, thin gray connecting lines for the tree edges.

Current attempt: `prefix_tree_sharding.svg` is hand-built, not Makie, same category as the other structural figures in this deck. The exact child counts (4 per split) and box counts in the top row are illustrative, chosen for a legible tree shape, not a literal rendering of all 256 shards or the real ~14-16 child count for the worst case. Feel free to adjust when polishing by hand, especially if the real build ends up producing a visibly different shape once it actually runs.
