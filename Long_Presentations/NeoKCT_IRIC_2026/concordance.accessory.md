# Figure: NeoKCT vs. BamQuery, every (peptide, sample) pair

Scatter on the "Does it agree with BamQuery?" slide. 351 peptides BamQuery could place × 22 thymic samples = 7,722 pairs, rphm on log axes with zeros in their own strip. 6,957 pairs are zero in both tools, 617 are non-zero in both, 72 only BamQuery, 76 only NeoKCT. Points coloured by whether BamQuery found one or several genomic positions for the peptide.

Data: c5_pairs_ds.tsv, written by export_c5_pairs.py with the same join as Manuscripts/NeoKCT/paper/scripts/C5_concordance_ds.py (Spearman reproduces at 0.888). Plotted by plot_concordance.jl.
