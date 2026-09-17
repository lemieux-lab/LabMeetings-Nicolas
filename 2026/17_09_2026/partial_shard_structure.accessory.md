# Figure: `_PartialShard`, one prefix shard of a partial table

Source: `src/StreamBuild.jl`, struct `_PartialShard` (kmers, row_id, offsets, pool_s, pool_c) built by `_RowPool`/`_intern_row!`.

What it should show: how a shard's k-mers point into a deduped pool of sparse rows, CSR-style.

Two linked pieces, side by side:

**Left: k-mers, sorted, each with a row pointer**

A vertical list of `kmers[]` entries (just show 5-6 as an example, sorted, label as "k-mer i"), each with an arrow to the matching entry in a parallel `row_id[]` column right next to it.

Key point to draw explicitly: **two different k-mers can point to the same `row_id`**. Pick 2 of your 5-6 example k-mers and route their arrows to the same row number. That's the shard-local dedup from `_intern_row!`: when two k-mers have byte-identical `(sample, count)` rows, `_RowPool`'s `Dict{Vector{UInt32}, UInt32}` returns the existing row id instead of storing the row twice. Worth calling out with the warm accent color (`#fab219`/`#e58468`) on those two shared arrows so it reads as "these two collapsed into one."

**Right: the CSR row pool**

- `offsets[]`: a short array of row-boundary indices into the flat pool (length n_rows + 1, 1-based, `offsets[1] == 1`)
- `pool_s[]` / `pool_c[]`: the flat, parallel (sample, count) arrays, chunked visually into segments matching consecutive `offsets` values, one segment per row

Draw arrows from each `row_id` value on the left to the matching `offsets[row_id]..offsets[row_id+1]-1` segment on the right, so the reader can trace: k-mer -> row_id -> offsets slice -> the actual (sample, count) pairs for that k-mer.

Caption underneath: "one prefix shard: sorted k-mers, each pointing via `row_id` into a shard-local CSR pool of deduped sparse rows"

Small legend note: this shard-local dedup is narrow and cheap (only rows identical *within this one shard* collapse), unlike the old design's whole-table dedup attempt that needed a dictionary sized in the tens of billions of entries at full cohort scale. Worth a one-line callout distinguishing "shard-local, cheap" from "whole-table, what OOM'd the old design" if there's room, since that distinction is also the point of the dedup-asymmetry slide later in the deck.

Style: match the other three figures in this folder, dark card (`#151f1b`), accent green (`#3ecfa2`/`#0d7d63`) for the normal flow, warm orange (`#fab219`) reserved for the "these collapsed" callout.

Current attempt: `partial_shard_structure.svg` in this folder is a first pass, hand-built (not Makie). Example uses 5 k-mers and 4 rows, one pair of k-mers shares a row. Real shards hold far more, so treat the counts as illustrative only.
