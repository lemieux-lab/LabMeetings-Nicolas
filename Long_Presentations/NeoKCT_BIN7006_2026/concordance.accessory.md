# Figure: NeoKCT vs. BamQuery, every (peptide, sample) pair

Scatter on the "Does it agree with BamQuery?" slide. 351 peptides BamQuery could place × 22 thymic samples = 7,722 pairs, plus a "not placed" column for the 199 peptides BamQuery couldn't place (4,378 pairs, 64 with NeoKCT reads, 12 at or above 8.55 rphm), rphm on log axes with zeros in their own strip. Points coloured by whether BamQuery found one or several genomic positions for the peptide. The not-placed column is a beeswarm (_swarm in plot_concordance.jl): horizontal spread is how many pairs sit at that level, not a value.

NeoKCT side uses suffix-anchored peptide queries (2026-11-20, PAPER_TODO.md A5 side note). Before that fix: 6,957 pairs zero in both, 617 non-zero in both, 72 only BamQuery, 76 only NeoKCT, Spearman 0.888. After: 6,947 / 685 / 4 / 86, Spearman 0.939 (0.983 on pairs non-zero in both). The 72 BamQuery-only pairs were mostly C-terminal peptides (RLATAPSEK alone was 16), whose prefix query is empty because the next codon is a stop.

Data: c5_pairs_ds.tsv, written by export_c5_pairs.py with the same join as Manuscripts/NeoKCT/paper/scripts/C5_concordance_ds_suffix.py (Spearman reproduces at 0.939). `python3 export_c5_pairs.py prefix` writes the pre-fix pairs to c5_pairs_ds_prefix.tsv. Plotted by plot_concordance.jl.
