# Figure: build_kct_streaming pipeline

What it should show: 4 stages left to right (or top to bottom on a narrow slide), connected by arrows, same content as the `.pipeline` numbered list in countslayer_summary.html §03 but as a real flow diagram instead of a list.

1. **Count, per wave**. Samples counted in waves of `wave_size` (default 100). Each sample's records scattered by prefix into shard files on local scratch, not NFS.
2. **Fold each shard**. Sort by k-mer, collapse into (sample, count) rows, dedup identical rows within that shard only.
3. **Hierarchical merge, interleaved with the waves**. Groups of `merge_fanin` (default 5) partials combine as soon as their inputs are ready, not only after the last wave. Callout: "disk stays O(merge_fanin) waves, not O(all waves))", this is the Aug 2026 fix that stopped the shared export from filling up mid-build.
4. **Streaming assembly**. Final merge across shards has no dedup dictionary. Rows pack straight into 64-k-mer blocks, blob streams to a temp file then into the finished `.kct`, never buffered whole in RAM.

Extra elements worth drawing:
- A feedback loop / side input into stage 3 labeled "existing .kct as a `seeds` entry" (a ready-made level-0 partial, so a prior checkpoint doesn't need recounting).
- A small annotation that every stage marks itself done, so `resume=true` (default) picks a killed build back up without redoing finished work. This is what let the Aug 28 crashes resume instead of restarting from scratch.
- Optionally, tag stage 3 with the specific fix: before Aug 2026 the merge only ran after all waves finished (O(n_waves) partials resident), now it's interleaved (O(merge_fanin) resident). If room, a tiny "before / after" inset under stage 3 showing the disk-footprint difference would land well next to the Aug 28 crash story.

Style: match `countslayer_block_format.svg` and `dedup_asymmetry.svg`, dark card (`#151f1b`), accent green (`#3ecfa2` / `#0d7d63`) for the main flow, warm orange/red (`#fab219` / `#e58468`) reserved for the callout/fix annotations so they visually stand out as "this is what broke and got fixed" rather than being part of the steady-state pipeline.

Current attempt: `build_pipeline.svg` in this folder is a first pass, hand-built (not Makie). It's a straightforward 4-box flow with the O(merge_fanin) callout on stage 3. The seeds-loop and resume annotation were left out of the first pass for space and are good candidates to add if you polish this by hand.
