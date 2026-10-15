# Figure: why single-strand counting undercounts

Revised 2026-10-14 after feedback that the first pass was confusing (arrows not lining up with their marks, an unexplained grouping of reads "above" vs "below" a line that carried no real meaning).

What it shows now: two panels, same 4 reads in both, one row per read so each read's arrow and its checkmark/X live on the same horizontal line, no implied grouping. A small "coding strand ->" label at the top of each panel gives a reference direction without a baseline that the reads would otherwise visually collide with.

**Panel A, "Single-strand counting (unstranded reads)".** 4 reads, 2 pointing with the coding strand, 2 pointing against it. This 50/50 split isn't illustrative license, GTEx's own RNA-seq libraries are confirmed unstranded (checked directly against GTEx's QC metadata, ~50% sense on both mates), so each read's orientation really is random. The panel title itself names "unstranded reads" rather than leaving that detail to a subtitle, since that's the actual cause of the undercount, not an incidental property of this example. Each row's mark sits in a fixed right-hand column regardless of which way that row's arrow points, so the eye reads straight down the mark column: check, X, check, X. Matching reads get a checkmark and count. Reversed reads get an X and are dropped.

**Panel B, "Double-strand counting (fixes the undercount)".** Same 4 reads, same arrow directions (still 2 pointing each way, this is the literal orientation of the sequenced reads and doesn't change). The only difference: every row now gets a checkmark, because each read's reverse complement is counted alongside the read itself, so which way the arrow happens to point no longer matters.

One footer line under both panels ties it together: same 4 reads, 2 match the coding strand and 2 don't, double-strand counts both.

Style: matches `build_pipeline.svg`'s dark card (`#151f1b`), green (`#3ecfa2`) for counted reads, orange/red (`#e58468`) for dropped ones in Panel A only.

Current attempt: `double_strand_counting.svg` is still hand-built, not Makie, same category as `build_pipeline.svg`. The fixed mark column (independent of arrow direction) is the main structural fix from the first pass. Feel free to adjust spacing by hand if it's still busy on the real projector.
