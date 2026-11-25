# Figure: true count vs. count returned, NeoKCT and REINDEER

Slide "Approximate was never an option", under the table. All 75,886 (k-mer, sample) pairs of the paper's B4 benchmark (20,000 nucleotide 31-mers × 200 GTEx samples), each tool against the Jellyfish truth that matches its own counting convention: forward strand for NeoKCT (its nucleotide mode counts literal forward k-mers), forward + reverse complement for REINDEER (canonical k-mers, GTEx is unstranded). One bubble per distinct (true, returned) pair, area proportional to how many pairs share it, green on the diagonal (exact), red off it. Zeros on both axes get their own strips.

NeoKCT: 98.5% exact, the misses are 1,112 small undercounts from the old build dropping N-containing reads, 100% when they are kept (rebuild in preparation). REINDEER: 18.0% exact. 42,028 pairs (55%) are k-mers seen once in that sample, which REINDEER's default (BCALM -abundance-min 2) drops at index time, so it returns 0. On the 33,858 pairs it keeps, 40.4% exact and 63.1% within 20%, the rest is unitig averaging.

History: the first version scored REINDEER against forward-only truth (9.82% on 59,037 pairs), which charged it for every antisense read, 5,361 pairs looked like false positives and were reverse-strand reads. Rescored 2026-11-24 by Manuscripts/NeoKCT/paper/scripts/B4_compute_accuracy_canonical.py.

Data: Manuscripts/NeoKCT/paper/results/B4_accuracy_canonical_per_pair.tsv. Plotted by plot_exactness.jl.
