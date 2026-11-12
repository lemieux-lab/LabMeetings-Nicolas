# Figure: merge logic, roots and shards

What it shows: the 25 counting waves (100 samples each) merged 5 at a time into 5 roots. Each root holds all 256 prefix shards, drawn as a grid (rows = roots, columns = shard index, 12 of 256 shown). Two orange columns stand for the oversized Leu/Ser shards. A gold outline marks one shard index across the 5 roots, "one shard = 5 files". A dashed arrow leads from it to the merge illustration: a single k-mer's row is the concatenation of its pieces from root 1 to root 5, in root order, with no re-sort, because roots cover disjoint ascending sample ranges. The right panel lists why uneven shards hurt assembly: 256 x 5 = 1,280 files, each worker takes one shard (5 files read fully plus a merged copy), up to 8 workers at once on adjacent shards, adjacent shards are the giants.

Real or derived numbers: 25 waves of 100 samples, merge fan-in 5, 5 roots, 256 shards, shard 82 at 198 GiB combined and others ~1 MB (October median per root). About 500 samples per root is derived (5 waves x 100). Illustrative: the 12 columns shown, which columns are orange, the example k-mer and its (sample, count) pieces.

Written from `_merge_shard_rows` and `_assemble_v4` in `src/StreamBuild.jl` and `ARCHITECTURE.md` steps 3 and 5. Starting point was the 17_09_2026 `build_pipeline.svg` style (dark card, green flow, orange for what went wrong), but the layout is new because that figure does not show roots or shards.

Style: dark card (#151f1b), green normal, orange oversized, gold for the highlighted shard, gray for neutral. All connectors use absolute coordinates, no nested transforms.
