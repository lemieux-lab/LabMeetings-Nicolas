# Grouped bar chart: is the signal real? Fraction of 103 peptides found in at least one GTEx
# sample with >= c reads, for three peptide sets (C7 random-occupancy control, double-strand table).
# Real numbers from PAPER_TODO.md C11 / paper/results/ds_rerun/C7_occupancy_ds_summary.json:
#   real ovarian MAPs (Zhao et al. 2020)       99.0 / 94.2 / 82.5 %
#   same residues shuffled (composition kept)  48.5 / 22.3 /  9.7 %
#   uniform random 10-mers                       1.9 /  0.0 /  0.0 %
# Run: julia --project=<LabMeetings root> plot_occupancy.jl

using CairoMakie

real = [99.0, 94.2, 82.5]
shuf = [48.5, 22.3, 9.7]
rand10 = [1.9, 0.0, 0.0]

col_bg = RGBf(0x15/255, 0x1f/255, 0x1b/255)
col_ink = RGBf(0xe8/255, 0xef/255, 0xec/255)
col_dim = RGBf(0x9d/255, 0xb3/255, 0xab/255)
col_real = RGBf(0x3e/255, 0xcf/255, 0xa2/255)
col_shuf = RGBf(0xe5/255, 0x84/255, 0x68/255)
col_rand = RGBf(0x5a/255, 0x6e/255, 0x66/255)

set_theme!(Theme(
    backgroundcolor=col_bg, textcolor=col_ink, fontsize=17,
    Axis=(backgroundcolor=col_bg, xgridcolor=(:white, 0.0), ygridcolor=(:white, 0.08),
          xtickcolor=col_dim, ytickcolor=col_dim, leftspinecolor=col_dim, bottomspinecolor=col_dim,
          xlabelcolor=col_ink, ylabelcolor=col_ink, xticklabelcolor=col_dim, yticklabelcolor=col_dim,
          titlecolor=col_ink, topspinevisible=false, rightspinevisible=false),
    Legend=(backgroundcolor=col_bg, framevisible=false, labelcolor=col_ink),
))

fig = Figure(size=(1100, 520))
ax = Axis(fig[1, 1],
    xticks=(1:3, ["≥ 1 read", "≥ 2 reads", "≥ 5 reads"]),
    ylabel="% of 103 peptides found in GTEx",
    title="103 peptides each: real tumor MAPs vs. scrambled vs. random")
xs = repeat(1:3, 3)
grp = vcat(fill(1, 3), fill(2, 3), fill(3, 3))
vals = vcat(real, shuf, rand10)
colors = [col_real, col_shuf, col_rand]
barplot!(ax, xs, vals, dodge=grp, color=colors[grp])
for (x, g, v) in zip(xs, grp, vals)
    text!(ax, x + (g - 2) * 0.27, v + 1.5, text=string(v, "%"), align=(:center, :bottom), color=col_ink, fontsize=14)
end
ylims!(ax, 0, 112)
Legend(fig[1, 2], [PolyElement(color=c) for c in colors],
       ["real ovarian MAPs", "same residues, shuffled", "random 10-mers"])
save(joinpath(@__DIR__, "occupancy.svg"), fig)
println("wrote occupancy.svg")
