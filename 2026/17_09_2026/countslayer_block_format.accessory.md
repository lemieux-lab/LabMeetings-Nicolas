# Figure: CountsLayer block format

What it should show: one 64-k-mer block inside `blob`, byte-aligned, starting at `block_ptr[b]`.

Three stacked rows, left to right:

1. **Header row**, four small fixed cells then one wider one: `nk` | `lbits` | `gbits` | `cbits` | `varint n_exc`
2. **Packed body row**, three segments sized roughly by how much space they take in a real block:
   - `nk x row length (lbits each)`, narrow
   - `T x sample gap (gbits each)`, medium, this is the bulk of the block
   - `T x count (cbits each)`, medium-large
3. **Exception row**, byte-aligned, one segment: `n_exc x [varint index, UInt32 value]`, visually distinct color (this is the overflow path for counts >= 65535)

Caption underneath: "block layout in `blob`, starting at `block_ptr[b]` (byte-aligned)"

Legend / callouts (small text below the diagram):
- **lbits**: width for the longest row in the block
- **gbits**: width for the largest sample-to-sample gap
- **cbits**: width for the largest count, capped at 16 bits. Anything >= 65535 (~0.001% of pairs) spills to the exception list

Style: dark card on the slide background, one accent color for the packed body segments, a contrasting warm color for the exception segment (it's the "escape hatch," should read as different). Match the palette already used in `dedup_asymmetry.svg` (`#3ecfa2` accent, `#fab219` warm, `#151f1b` background, `#e8efec` ink, `#9db3ab` dim text) so it sits next to that plot without clashing.

Current attempt: `countslayer_block_format.svg` in this folder is a first pass at this, hand-built (not Makie). Proportions are illustrative, not measured from a real block, worth eyeballing against an actual block dump before using it live if you want the segment widths to mean something.
