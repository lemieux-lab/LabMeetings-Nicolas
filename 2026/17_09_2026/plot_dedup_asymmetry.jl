# Grouped bar chart: why a cross-k-mer dedup pool wasn't worth it in CountsLayer V4.0.
# Two row-length buckets, measured on real GTEx data (see countslayer_summary.html §02).
# Short rows (<=4 pairs) hold ~4% of all pairs but dedup ~12x.
# Long rows (>4 pairs) hold ~96% of all pairs but dedup only ~1.0x (basically unique).
# Run: julia --project=<LabMeetings root> plot_dedup_asymmetry.jl

using CairoMakie

buckets = ["<= 4 pairs/row", "> 4 pairs/row"]
share_of_pairs = [4.0, 96.0]   # percent of all (sample, count) pairs
dedup_ratio = [12.0, 1.0]      # measured dedup factor

col_bg = RGBf(0x15/255, 0x1f/255, 0x1b/255)
col_ink = RGBf(0xe8/255, 0xef/255, 0xec/255)
col_dim = RGBf(0x9d/255, 0xb3/255, 0xab/255)
col_share = RGBf(0x3e/255, 0xcf/255, 0xa2/255)
col_ratio = RGBf(0xfa/255, 0xb2/255, 0x19/255)

set_theme!(Theme(
    backgroundcolor=col_bg,
    textcolor=col_ink,
    Axis=(backgroundcolor=col_bg, xgridcolor=(:white, 0.06), ygridcolor=(:white, 0.06),
          xtickcolor=col_dim, ytickcolor=col_dim, leftspinecolor=col_dim, bottomspinecolor=col_dim,
          xlabelcolor=col_ink, ylabelcolor=col_ink, xticklabelcolor=col_dim, yticklabelcolor=col_dim,
          titlecolor=col_ink),
))

fig = Figure(size=(760, 440))
ax = Axis(fig[1, 1],
    xticks=(1:2, buckets),
    ylabel="share of pairs (%)  /  dedup ratio (x)",
    title="Dedup asymmetry by row length")

barplot!(ax, [0.8, 1.8], share_of_pairs, width=0.35, color=col_share, label="share of all pairs (%)")
barplot!(ax, [1.2, 2.2], dedup_ratio, width=0.35, color=col_ratio, label="dedup ratio (x)")

for (x, v) in zip([0.8, 1.8], share_of_pairs)
    text!(ax, x, v + 2, text="$(v)%", align=(:center, :bottom), color=col_ink, fontsize=15)
end
for (x, v) in zip([1.2, 2.2], dedup_ratio)
    text!(ax, x, v + 2, text="$(v)x", align=(:center, :bottom), color=col_ink, fontsize=15)
end

ylims!(ax, 0, 105)
axislegend(ax, position=:rt, backgroundcolor=col_bg, labelcolor=col_ink)

out_path = joinpath(@__DIR__, "dedup_asymmetry.svg")
save(out_path, fig)
println("wrote ", out_path)
