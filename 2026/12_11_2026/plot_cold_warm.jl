# Bar chart: per-query latency on the double-strand table, log scale.
# Numbers from B2 (ds_rerun/B4_mmap_detailed_ds.json and the NeoKCT B2 table):
#   warm lookup, location only: 24.8 us (1 thread)
#   warm decode of an already-touched block: ~61 us
#   cold decode, first touch of a never-read block: mean 16,799 us (median 16,606 us)
# Run: julia --project=<LabMeetings root> plot_cold_warm.jl

using CairoMakie

labels = ["Lookup\n(location only)", "Warm decode\n(block already paged in)", "Cold decode\n(first touch, mmap)"]
us = [24.8, 61.0, 16799.0]

col_bg = RGBf(0x15/255, 0x1f/255, 0x1b/255)
col_ink = RGBf(0xe8/255, 0xef/255, 0xec/255)
col_dim = RGBf(0x9d/255, 0xb3/255, 0xab/255)
col_ok = RGBf(0x3e/255, 0xcf/255, 0xa2/255)
col_bad = RGBf(0xe5/255, 0x84/255, 0x68/255)

set_theme!(Theme(
    backgroundcolor=col_bg,
    textcolor=col_ink,
    Axis=(backgroundcolor=col_bg, xgridcolor=(:white, 0.0), ygridcolor=(:white, 0.08),
          xtickcolor=col_dim, ytickcolor=col_dim, leftspinecolor=col_dim, bottomspinecolor=col_dim,
          xlabelcolor=col_ink, ylabelcolor=col_ink, xticklabelcolor=col_dim, yticklabelcolor=col_dim,
          titlecolor=col_ink),
))

fig = Figure(size=(900, 480))
ax = Axis(fig[1, 1],
    xticks=(1:3, labels),
    yscale=log10,
    ylabel="latency per query, µs (log scale)",
    title="Double-strand table, mmap only (2.15 TiB, does not fit in RAM)")

barplot!(ax, 1:3, us, width=0.55, color=[col_ok, col_ok, col_bad])
txt = ["24.8 µs", "~61 µs", "~17 ms"]
for (i, v) in enumerate(us)
    text!(ax, i, v * 1.5, text=txt[i], align=(:center, :bottom), color=col_ink, fontsize=16)
end
ylims!(ax, 5, 120000)

out_path = joinpath(@__DIR__, "cold_warm_latency.svg")
save(out_path, fig)
println("wrote ", out_path)
