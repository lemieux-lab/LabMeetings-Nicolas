# Briefing for lab meeting prep, 2026-10-15

Written 2026-10-14 for a fresh Claude session to pick up and help build the actual lab meeting deck. This is context, not slides. Read [[project_lab_meetings]] conventions before drafting anything.

## How to use this document

Nicolas has a lab meeting tomorrow (2026-10-15) and wants an update deck covering what's happened since the last one (2026-09-17). This file is the handoff: everything a new session needs to know without re-deriving it from scratch. The previous deck is at `../17_09_2026/lab_meeting.qmd` — read it first for exact prior slide structure, tone, and the project_lab_meetings conventions (Quarto revealjs, 1920x1080, dark theme, technical bioinformatician audience, tables/plots over prose, SVG figures with accessory files).

**The last deck's own "what's next" slides (for a direct callback):**
- Engineering "Near" item: *"Stream `blob` during DNA assembly, currently RAM-resident, peak ~1.5 TB."* This is now the single biggest open problem (see the rebuild crash saga below) — worth flagging explicitly that the risk called out a month ago is exactly what's biting now.
- "Now": compare the pipeline against BamQuery on the GTEx cohort — this became the C0-C10 analysis arc described below, now mostly done.
- "Next"/"Later": nucleotide-mode REINDEER benchmark, k4neo junction ground truth, CLDN18/CTA reproduction, construction-memory benchmarking — all still genuinely open, not started.

## Standing instructions relevant to any update prep

- Writing style (applies to all prose on slides): no em dashes, no semicolons, no "delve"/"moreover"/"furthermore"/"albeit"/"indeed", no "not X but Y", no rhetorical question-answer pairs, no parallel triples, no bullet-where-a-sentence-would-do, no decorative headers, minimal bold/italic, no cliché metaphors.
- Slides: concise text, series of values go in a table not prose, propose a plot (with Julia code) where a plot reads better than a table, prefer an SVG figure over text for structure/pipeline/concept slides and always write an accessory `.md` file describing the intended figure logic even if the SVG itself isn't hand-finished.
- Only commit to git when explicitly asked. Don't be proactive about pushing/committing the deck itself unless told to.
- The user's email (nicolas.jacquin@gmail.com) is for attribution only, never send it anywhere.

## Part 1: Manuscript status (the main substantive progress)

The NeoKCT manuscript ("NeoKCT: exact per-sample k-mer abundance across healthy-tissue cohorts for reference-free, quantitative screening of tumor-specific antigens", Jacquin & Lemieux) is essentially fully drafted as of 2026-09-29: Abstract, all of Methods, Results 3.1 through 3.5, Figure 3 and Figure 4's panel captions and legends, and the Discussion are all filled with real numbers. Remaining manuscript gaps: Figure 1 panel D's caption (open question whether to keep that panel at all), the Zenodo DOI line in Data Availability (blocked on an actual deposit, archive already prepared at `paper/NeoKCT_zenodo_archive.zip`), the funding statement (needs Lemieux's grant number), and hardware specs for muninn (needs IT/admin access Nicolas has that this session doesn't).

Since the last lab meeting, the following analyses were completed and written into the draft:

**C8/C10 — real ovarian tumor cohort, now fully built and analyzed (new since Sep 17).** A 9-sample ovarian tumor RNA-seq cohort (GEO GSE131880, matching the lab's own 9 mass-spec samples) was downloaded and built into a NeoKCT table (3.88B k-mers, 6.52B pairs, 27.16 GB), after a genuinely hard build saga worth mentioning on its own merits:
- Found and fixed a real memory leak in `JelloFish.jl`'s counting kernel: a `Task[]` vector retained every merge task's closure forever for no functional reason, so peak memory scaled with cumulative merges done, not final table size. This explained why repeated attempts at this build kept OOMing at different, seemingly random points, and why 1TB wasn't enough for even a single deeply-sequenced sample.
- One source FASTQ (SRR9141174_2) was corrupted at ENA (reproduced identically on a fresh re-download, ruling out a transfer glitch), worked around by sourcing the same run from NCBI SRA instead.
- A home-directory quota exhaustion and a node-locality confusion (this session's shell runs on a different physical node than the Slurm jobs it submits) were both diagnosed and resolved along the way.

Once built, the tumor table was queried against the 103 real published ovarian aeTSA/mTSA peptide candidates (Zhao et al. 2020) and cross-referenced with the existing GTEx and DC/mTEC healthy-tissue references. Headline results now in the manuscript:
- 91/103 (88.3%) show direct RNA-level support in their own source tumors, a strong positive control.
- 38/103 remain specific against both GTEx and the DC/mTEC second reference.
- 29/103 satisfy both tumor detection and dual-reference specificity at once, the cleanest candidate set.
- 8/103 meet a published two-fold tumor-overexpression TAA criterion (Apavaloaei et al. 2025).
- 12/103 show no RNA support in any tumor sample at all.

**C9 — second healthy-tissue reference (new since Sep 17).** Realized the existing 22-sample small cohort (19 blood DC + 3 mTEC, already built for the BamQuery comparison) doubles as BamQuery's own canonical reference panel, so it was reused as an independent specificity check on the same 103 candidates without any new sequencing data needed. About 40% of the 103 candidates would be called differently depending on which single reference (GTEx alone vs. this second one alone) a screen used, underscoring why checking against multiple healthy-tissue sources matters.

**Runtime/cost comparison against BamQuery, now finalized with real numbers.** BamQuery's own published cost is 729.6 CPU-hours for their full GTEx run. NeoKCT's one-time build cost is 227.3 hours (9.47 days), after which each query session costs only 43.9 minutes, about 31x faster than BamQuery's published figure and 56x faster than a same-machine extrapolation of BamQuery's own cost. This is the core "build once, query forever" argument for the paper, now backed by measured numbers on both sides rather than an estimate.

**Licensing and attribution resolved:** Apache 2.0 license chosen and added to the repo (permissive, explicit patent grant). dbGaP data-use terms researched: the per-sample k-mer table almost certainly counts as a "data derivative" under GTEx's controlled-access terms (not a pure summary statistic), meaning the recipe/code can be public but the table itself needs controlled-access distribution, matching what was already suspected. Still needs final confirmation against the lab's actual signed agreement, which only Nicolas/the lab can do.

**Still genuinely open, not started:** the k4neo junction ground-truth benchmark (148 samples, 3,705 splice junctions, would need a new dataset acquisition and a build comparable in scope to the GTEx rebuild below, explicitly deferred pending a decision on priority), the nucleotide-mode apples-to-apples REINDEER benchmark, and reproducing k4neo's own CLDN18/CTA expression analyses with real per-sample counts.

## Part 2: The GTEx double-strand rebuild (the live, in-progress story)

This is likely the single most discussion-worthy item for tomorrow, both because it's substantively important (fixes a real undercounting bug affecting the whole paper's GTEx reference) and because it's been a genuinely difficult, still-unresolved engineering problem live as of this writing.

**Why it's happening:** after a conversation with Lemieux, it became clear the production GTEx table (2,487 samples, built single-strand) was undercounting true supporting reads for any peptide in a reverse-stranded or unstranded RNA-seq library, since single-strand counting only credits a read if it happens to match the expected coding strand. Double-strand counting (counting each read's reverse complement alongside the read itself) fixes this, and is what BamQuery and most comparable tools effectively assume. This directly affects the C2 GTEx-scale reproduction-of-BamQuery-statistics result and arguably several other sections, so a full GTEx rebuild in double-strand mode was judged necessary before the paper is truly final, rather than a nice-to-have.

**What's new since Sep 17, chronologically:**
1. A 200-sample pre-flight test de-risked the parameters first, and in the process found two real latent bugs in the original production build script (a dead module reference and a wrong Julia project path) that would have caused a silent failure partway through a multi-week run if not caught first. Both fixed and validated with a smoke test before committing.
2. The real rebuild (job 8113269, started 2026-10-06) failed on its very first wave with a disk-space exhaustion, traced to unrelated leftover data on the shared compute node (not a double-strand-specific problem), cleaned up and resubmitted.
3. The resubmitted job (8113291) ran cleanly through all 25 waves and all 5 hierarchical merges over about 8 days, confirming the production architecture's merge-memory ceiling holds steady (~1,500 GB peak) regardless of how far into the run a merge happens, a real, previously-unconfirmed property.
4. One real sample (SRR5125583, GTEx lung) turned out to have been deleted from the shared source export sometime after the original single-strand build completed (a pre-existing, previously-documented gap, not new). The job was cancelled and resubmitted against a corrected 2,486-sample list (one fewer than the original 2,487) rather than wasting hours on inevitably-failing retries, with resume logic correctly skipping all already-completed work.
5. All 25 waves and all 5 merges completed successfully. **Final assembly, the single step that holds the full cohort's unique k-mer array in RAM at once, is the one stage that has not yet succeeded.** Three consecutive attempts have OOM-killed partway through, despite escalating the Slurm memory request each time (1,500 GB -> 1,650 GB -> 1,800 GB, using the node's full available headroom each time with Nicolas's explicit go-ahead to not reserve room for other users until this finishes). Notably, a 300 GB memory increase between attempts 1 and 3 barely moved the crash point at all, arguing against "simply needs more total memory" as the root cause. The current hypothesis, being tested in a fourth attempt running right now, is that the assembly step's internal concurrency (`W = clamp(threads, 1, 8)`, a merge window over shards) was pinned at its maximum the whole time across all three failures (all used `--cpus 24`, far more than the clamp ceiling), and that fewer shards processed concurrently may reduce the peak transient memory spike rather than relying on more total memory to outrun it. This fourth attempt uses `--cpus 6`.

**As of writing this brief (2026-10-14, ~08:46 EDT), job 8117738 is running, about 5 minutes in, memory still low. Check its current status before the meeting** — if it has progressed past roughly 56/256 shards (the point all three prior attempts died at) that is a strong positive signal; if it crashed again, that rules out the concurrency-window hypothesis too and the next step would mean reading the assembly code itself (`_assemble_v4` / `_merge_shard_rows` in `src/StreamBuild.jl`) for a real fix rather than further parameter tuning.

**Framing suggestion for the deck:** this is a good "science in progress" slide, not something to hide. The pre-flight de-risking, the two caught bugs, the clean 25-wave/5-merge run, and the honest ongoing assembly-memory puzzle all demonstrate real engineering rigor. The exact callback to last month's own "Near" item ("stream blob during assembly, peak ~1.5 TB") landing almost exactly on the mechanism now causing trouble is a strong, honest narrative beat.

## Part 3: Suggested rough structure for tomorrow (not a final decision, just a starting point)

1. Recap slide, one line per major Sep-17-to-now development (mirrors "Recap · Where July 30 Left Off" style from the last deck)
2. Manuscript status: essentially fully drafted, real numbers in, short list of what's left
3. New results slide(s): C8 tumor cohort + C10 tumor-vs-normal headline numbers (table, not prose)
4. C9 second-reference finding (the ~40% reclassification number is a strong one-liner)
5. The rebuild story: why double-strand matters, the clean 25-wave/5-merge run, the honest unresolved assembly-memory problem, current live status
6. Updated "what's next" slide, correcting/updating the Sep-17 one

## Where to find things

- Manuscript draft: `NeoKCT_manuscript_draft_v0.1.docx` (repo root of Manuscripts/NeoKCT)
- Task tracker with full detail on every analysis: `PAPER_TODO.md` (same directory) — long, grep for `C8`, `C9`, `C10` rows for the fullest detail
- Rebuild logs: `paper/results/logs/D3_full_rebuild_ds_2486_retry3.<jobid>.log` (current attempt) and its retry/retry2 siblings for history
- Live status check: `sacct -j 8117738 --format=State,Elapsed,ExitCode` and `tail` the log above
- A standing status doc on the rebuild (more granular blow-by-blow than this brief) lives as a Claude Docs artifact Nicolas can reopen: `https://claude.ai/artifact/PmUhKnBJzZy1DJP6aFS4io`
