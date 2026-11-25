#!/usr/bin/env python3
# Dumps the 7,722 placed (peptide, sample) pairs, plus the 4,378 for peptides BamQuery couldn't place, behind the "Does it agree with BamQuery?" slide, so
# plot_concordance.jl can draw them. The join is copied from the paper's
# Manuscripts/NeoKCT/paper/scripts/C5_concordance_ds.py (double-strand rerun), which only keeps
# the pairs in memory. Same inputs, same rphm denominator (manifest primary reads), same universe
# (real peptides BamQuery could place). Also carries how many genomic positions BamQuery found
# per peptide, since multi-origin peptides are where the two tools disagree most.
# Since 2026-11-20 the NeoKCT side is the suffix-anchored rerun (peptide_counts anchor=:both,
# paper/results/ds_suffix/), the version on the slide. Pass "prefix" to dump the old one.
# Run: python3 export_c5_pairs.py
import os
from collections import defaultdict
import openpyxl

PAPER = "/u/jacquinn/phd_stuff/Manuscripts/NeoKCT/paper"
RESULTS = f"{PAPER}/results"
MANIFEST = f"{RESULTS}/C3_neokct_sample_manifest.tsv"
C1_PEPTIDES = f"{RESULTS}/C1_peptides.tsv"
import sys
PREFIX_ONLY = "prefix" in sys.argv[1:]
C4_SMALLCOHORT = (f"{RESULTS}/C4_neokct_ds_smallcohort.tsv" if PREFIX_ONLY
                  else f"{RESULTS}/ds_suffix/C4_neokct_ds_smallcohort_suffix.tsv")
BAMQUERY_XLSX = f"{PAPER}/data/output/res/C3_smallcohort_count_norm_info.xlsx"
REAL_SETS = {"dlbcl_cta", "dlbcl_tsa", "mutated_ta", "ovarian_aeTSA", "ovarian_mTSA"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c5_pairs_ds_prefix.tsv" if PREFIX_ONLY else "c5_pairs_ds.tsv")

sample_lib = {}
with open(MANIFEST) as f:
    for line in f:
        if line.startswith("#") or line.startswith("slot"):
            continue
        slot, sample_id, tissue, primary_reads = line.rstrip("\n").split("\t")
        sample_lib[sample_id] = float(primary_reads)

pep_set = {}
with open(C1_PEPTIDES) as f:
    for line in f:
        if line.startswith("#") or line.startswith("pep\t"):
            continue
        pep, length, set_, *_ = line.rstrip("\n").split("\t")
        pep_set.setdefault(pep, set_)
real_peps = {p for p, s in pep_set.items() if s in REAL_SETS}

wb = openpyxl.load_workbook(BAMQUERY_XLSX, read_only=True)
rows = list(wb["Read count RNA-seq by peptide"].iter_rows(values_only=True))
bq_cols = [h[len("bam_"):] for h in rows[0][2:]]
bq_counts = {r[1]: dict(zip(bq_cols, r[2:])) for r in rows[1:]}
pep_positions = defaultdict(set)
for r in wb["Alignments Read count RNA-seq"].iter_rows(min_row=2, values_only=True):
    pep_positions[r[1]].add(r[2])
wb.close()

nk_counts = defaultdict(dict)
with open(C4_SMALLCOHORT) as f:
    for line in f:
        if line.startswith("#") or line.startswith("pep\t"):
            continue
        pep, slot, sample_id, tissue, count, rphm = line.rstrip("\n").split("\t")
        nk_counts[pep][sample_id] = int(count)

universe = sorted(real_peps & bq_counts.keys())
n = 0
with open(OUT, "w") as out:
    out.write("pep\tsample\tset\tn_positions\tbq_count\tnk_count\tbq_rphm\tnk_rphm\n")
    for pep in universe:
        for s, lib in sample_lib.items():
            bq_c = bq_counts[pep].get(s, 0) or 0
            nk_c = nk_counts.get(pep, {}).get(s, 0)
            out.write(f"{pep}\t{s}\t{pep_set[pep]}\t{len(pep_positions.get(pep, ()))}\t{bq_c}\t{nk_c}\t"
                      f"{bq_c / lib * 1e8}\t{nk_c / lib * 1e8}\n")
            n += 1
    # Peptides BamQuery couldn't place in GRCh38 have no BamQuery count at all (not zero, absent),
    # so bq_count is NA and n_positions is 0. NeoKCT still counts them.
    unplaced = sorted(real_peps - bq_counts.keys())
    for pep in unplaced:
        for s, lib in sample_lib.items():
            nk_c = nk_counts.get(pep, {}).get(s, 0)
            out.write(f"{pep}\t{s}\t{pep_set[pep]}\t0\tNA\t{nk_c}\tNA\t{nk_c / lib * 1e8}\n")
            n += 1
print(f"wrote {n} pairs, {len(universe)} placed + {len(unplaced)} unplaced peptides x {len(sample_lib)} samples to {OUT}")
