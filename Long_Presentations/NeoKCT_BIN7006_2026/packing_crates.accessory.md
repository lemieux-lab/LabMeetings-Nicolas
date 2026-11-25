# Figure: drop the leading zeros

Top row: eight counts from one block as plain 32-bit numbers, drawn as zero-padded 10-digit decimals. Second row: the same counts packed at 3 bits each because the block's largest count is 6 (110 in binary). Box widths to scale (3.5 px per bit), gaps between boxes are not. Bottom: the whole GTEx table as bars to scale, 7.08 TiB as plain lists (7.78 TB, 909.7 B (sample, count) entries at 4 + 4 bytes plus 8 bytes per fragment) against the real 2.15 TiB, 70% smaller. That 70% is gaps and packing together, same numbers as the old 8.5 vs 2.6 bytes per entry.

Trimmed for BIN7006: one subtitle per row (32 bits, room for 4.3 billion / 3 bits, enough for this block), one line on why the width is chosen per block (every count stays findable at position × width), and the GTEx result bars labelled plain lists vs. with gaps + packing.
