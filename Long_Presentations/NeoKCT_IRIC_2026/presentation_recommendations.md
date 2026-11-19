# Presentation recommendations

Speaker notes for presentation.qmd, slide by slide, in presentation order.

## Overall timing (title slide)

~23.5 min total. Problem ~10 min, approach ~2.5 min, under the hood ~5 min, accuracy ~3 min, what it enables ~2.5 min, summary ~1 min. If running long, the gaps slide and the leading-zeros slide are the easiest to skip.

## Where MHC-I peptides come from

~1.5 min. Start from what everyone here does: peptides off MHC-I, identified by MS against a database built from the tumor's own RNA-seq. Canonical peptides have a gene model behind them. The non-canonical ones, which are most of the TSAs, don't, so tracing them back to their RNA is the hard part, and that is exactly the next question for any candidate.

## The question behind every TSA project

~1 min. Everyone in the room knows these two questions. The point to land is the last sentence: since the candidates change every project, the answer has to be ready for any peptide, which means for any read.

## How much data that is

~1 min. The full grid is 155 trillion values, 99.4% of them zero. Keeping only the non-zero values still gives 7.8 TB. Point at the dashed line and say the next slide explains why memory, and not disk space, is the limit that matters.

## Why it has to fit in memory

~1 min. Most of the audience won't have thought about this, keep it concrete. Disk is huge and cheap but every random visit is a trip downstairs. Memory is small and expensive but instant. Fast peptide lookup depends on two things: a layout that keeps related entries together, and keeping the randomly accessed parts in memory. That's why every tool on the next slide is really fighting to shrink what has to sit in memory.

## What existing tools give up to fit in memory

~1.5 min. Frame each row as a deliberate trade, not a flaw: these are good tools that each chose what to drop so the data would fit. Gene tables drop everything outside annotation. BamQuery drops precomputation and pays per question instead. REINDEER merges counts of neighbouring k-mers into one value per unitig. Raptor keeps a bit per sample in Bloom-filter-like structures, which costs some false positives. Next slide says why none of them are safe for a TSA screen.

## Why approximate isn't safe for TSAs

~1.5 min. This is what refusing approximations buys. The first row is the dangerous one: a silent zero. No reads from a gene table or an unplaceable peptide looks identical to "not expressed". The second row is the expensive one: losing a good candidate late. REINDEER can make both mistakes, Raptor the second and can't do thresholds at all, gene tables and BamQuery's unplaced peptides the first. Exact counts leave the biology as hard as it was, and stop the tool from adding errors of its own on top.

## A closer look at BamQuery

~2 min. BamQuery's compromise isn't arbitrary, it's forced by the direction of translation. Going backward from a peptide explodes, about 3.6 codons per residue, so hundreds of thousands of DNA sequences for a 9 or 10-mer. Too many to search the reads for, so the reference genome narrows them down first, and every new list re-reads every BAM. Bottom lane: going forward from the reads has exactly one answer per window, which is what makes counting everything once possible. Don't go further into the bottom lane yet.

## No compromises

~1 min. The main idea of the talk, say it slowly. The orange bars are what the naive versions cost. NeoKCT is 2.4 TB, right at the edge of the server's memory. The design splits it along the line from the previous slides: the randomly accessed index stays on the desk, and the counts are laid out so one basement trip serves many lookups (the library slide later shows this). Every project asks GTEx the same question with a different list, so paying for the build once is the right trade. Exact counts are the part we refused to trade away, hence the title.

## Cut every read into fragments, count them all

~2 min. Walk the figure left to right. Each read is cut into 30-nucleotide windows at every position, each window is translated into a 10-amino-acid fragment (stop codons drop the window), and we count how many times each fragment appears in each sample. No alignment, no annotation. The result is a giant table: rows are fragments, columns are samples. Most values are zero and cost nothing.

## The table, built once for GTEx

~1 min. Big numbers, but the takeaway is the last two rows: built once, then each lookup is microseconds.

## Store it like a search engine

~1.5 min. Everyone has used a search engine. It doesn't keep a giant grid of every word against every web page, it keeps, for each word, the short list of pages containing it. Our table is the same idea: for each fragment, the list of samples it was seen in, with the count. 99.4% of the fragment-by-sample grid is empty, so this alone is the difference between impossible and possible.

## Drop the leading zeros

~1 min. Counts are stored in blocks of 64 fragments. Each block looks at its largest count and gives every count in the block exactly that many bits, here 3 because the largest is 6. Same width for the whole block, so you can still jump straight to any entry. Net effect on the whole table: 7.8 TB as plain lists, 2.4 TB packed. The block is also the unit we read from disk, which comes back on the library slide.

## Write down only the gaps

~1 min. Start from the right panel's first line: to the computer, a fragment is a number, each residue a 5-bit digit. Sorting the table alphabetically sorts those numbers, so they only ever increase, like times at a finish line. Neighbours are close, so we write the full number once every 256 fragments and only the small gap in between. The finish-line times are made up to match the real gaps of these four fragments.

## A library, not a warehouse

~1.5 min. Cold fetch ~17 ms, already-fetched ~61 µs. Because a peptide query touches neighbors, most lookups are already in hand: 1,245 peptides against 2,486 samples in 0.5 s of lookup, after ~45 min of loading the catalog. Random lookups scattered everywhere would pay the full cost each time, peptide queries don't.

## Approximate was never an option

~1.5 min. This is the title of the talk, and it closes the loop on the existing-tools slide from the intro. The safety question is decided by rare, low, sample-specific expression. An index that averages counts over a unitig smears a single sample's 3 reads across its neighbors, or drops them. We chose to pay for exactness with engineering instead of with accuracy.

## Does it agree with BamQuery?

~1.5 min. Same numbers on the same scale: the fitted ratio between the two tools is exactly 1, so the 8.55 rphm threshold carries over unchanged (a cross-validated threshold lands at 8.06). The 199 peptides BamQuery could not place are still queryable here. This is the evidence behind the next slide's claim.

## Replacing BamQuery for expression screening

~1.5 min. This is the slide for the biochemists: what they would actually do with it, and the honest boundary. NeoKCT answers the screening question faster and for more peptides. It does not attribute reads to a genomic locus, because there is no alignment.

## A tumor cohort through the same pipeline

~1 min. 17 candidates are both detected in their own tumors and specific against both references: that's the short list a biochemist would take forward.

## Summary

~1 min. The left column is what everyone in the room lives with now, the right column is what changes. The last two rows are where this goes next rather than results shown today, say so. End on the manuscript.

## What that costs in practice

~1 min. Make the "every question is a new run" point land. In a discovery project you ask dozens of questions.

## Cost of a new question

~1 min. Log scale. The gold bar is what a new question costs including loading, the green one is the lookup itself.

## Is the signal real?

~1.5 min. If the table were just noise or composition bias, shuffled peptides would score like real ones. They don't. Random 10-mers: 1.9% at one read (2 of 103), 0 above that, close to what chance predicts.

## Two healthy references catch different things

~1 min.

## Where this goes next

~1 min.

## Querying a peptide

For questions. MHC-I peptides are 8 to 11 long, the table holds 10-mers. Shorter peptides: every 10-mer that starts with the peptide sits next to the others in the sorted table, add them up. This mirrors BamQuery's requirement that a read spans the whole coding sequence. Longer: overlapping tiles, take the minimum. Only blind spot worth naming: a peptide at the very end of its protein has no room for the extra residues, about 0.85% of MAPs.

## Reads can come from either strand

For questions. A library-prep detail that would change counts by about 2x if ignored.
