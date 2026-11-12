# Figure: patch_sample_counts

What it shows: the data flow of `patch_sample_counts` in StreamBuild.jl. The assembled table (left, top) and a corrected single-sample recount (left, bottom) both feed one streaming pass. That pass decodes each 64-k-mer block once, merge-walks it against the recount, and re-encodes once. Three outcomes come out, each with its real count from the slot 289 patch: 292,900,277 existing rows updated in place, 42,550,485 rows added where the sample had no entry, and 0 rows needing a scrub. All three feed a new output file (the input is never mutated).

Real numbers: all counts, the ~35 h runtime, and the 62.56 B final k-mer total. Illustrative: box sizes and positions only.

Style: dark card (#151f1b), green for kept or corrected rows, gold for the one corrected input, gray for neutral steps. All connectors use absolute coordinates, no nested transforms, so no offset bug is possible.

Current attempt: first pass, hand-built. Polish spacing by hand if it looks busy on the projector.
