# Log-scale bar chart: assembly's 256 shards are wildly uneven in size.
# A k-mer is bucketed by its top 8 bits (~1.6 leading amino acids of a 10-residue k-mer).
# Amino acid usage in real proteins is far from uniform, so a handful of shards
# (common leading residues) balloon while most stay tiny.
# Exact per-shard sizes aren't measured, only the two summary figures below
# (median ~1 MB, giant shards 25-42 GB) -- illustrative, not a real distribution.
# Run: julia --project=<LabMeetings root> plot_shard_skew.jl

using CairoMakie

labels = ["Typical shard\n(~250 of 256)", "Giant shard\n(a handful)"]
size_mb = [1.0, 32000.0]   # 1 MB vs ~32 GB (geometric-ish midpoint of the 25-42 GB range)

col_bg = RGBf(0x15/255, 0x1f/255, 0x1b/255)
col_ink = RGBf(0xe8/255, 0xef/255, 0xec/255)
col_dim = RGBf(0x9d/255, 0xb3/255, 0xab/255)
col_typ = RGBf(0x3e/255, 0xcf/255, 0xa2/255)
col_giant = RGBf(0xe5/255, 0x84/255, 0x68/255)

set_theme!(Theme(
    backgroundcolor=col_bg,
    textcolor=col_ink,
    Axis=(backgroundcolor=col_bg, xgridcolor=(:white, 0.0), ygridcolor=(:white, 0.08),
          xtickcolor=col_dim, ytickcolor=col_dim, leftspinecolor=col_dim, bottomspinecolor=col_dim,
          xlabelcolor=col_ink, ylabelcolor=col_ink, xticklabelcolor=col_dim, yticklabelcolor=col_dim,
          titlecolor=col_ink),
))

fig = Figure(size=(760, 460))
ax = Axis(fig[1, 1],
    xticks=(1:2, labels),
    yscale=log10,
    ylabel="shard size, MB (log scale)",
    title="256 shards, split by an 8-bit k-mer prefix")

barplot!(ax, 1:2, size_mb, width=0.5, color=[col_typ, col_giant])

text!(ax, 1, size_mb[1] * 1.6, text="~1 MB", align=(:center, :bottom), color=col_ink, fontsize=16)
text!(ax, 2, size_mb[2] * 1.6, text="25-42 GB", align=(:center, :bottom), color=col_ink, fontsize=16)

ylims!(ax, 0.3, 200000)
out_path = joinpath(@__DIR__, "shard_skew.svg")
save(out_path, fig)
println("wrote ", out_path)
