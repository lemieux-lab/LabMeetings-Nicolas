# Horizontal bars, log scale: CPU-hours to check one peptide list against all of GTEx.
#   BamQuery, published GTEx run: 729.6 CPU-h (Ruiz Cuevas et al. 2023)
#   BamQuery, our hardware, scaled to GTEx: ~1,301.6 CPU-h (measured on the 22-sample cohort,
#     14.3 CPU-h... scaled up; extrapolated, see LabMeetings 15_10_2026 "Build Once, Query Forever")
#   NeoKCT, full session on the double-strand table: 45.6 min wall on 16 threads, so at most
#     12.2 CPU-h (upper bound: 16 x 0.76 h, mostly I/O-bound table loading)
#   NeoKCT, lookup alone for 1,245 peptides: 0.5 s wall on 16 threads, so at most 8 CPU-seconds
# Run: julia --project=<LabMeetings root> plot_cost.jl

using CairoMakie

labels = ["BamQuery, published\nGTEx run", "BamQuery, our server,\nscaled to GTEx*",
          "NeoKCT, whole session\n(load + query)**", "NeoKCT, lookup only"]
cpuh = [729.6, 1301.6, 12.2, 16 * 0.5 / 3600]  # lookup: 0.5 s wall x 16 threads, upper bound
txt = ["729.6 CPU-h", "~1,301.6 CPU-h", "≤ 12.2 CPU-h", "≤ 8 CPU-seconds (0.5 s wall)"]

col_bg = RGBf(0x15/255, 0x1f/255, 0x1b/255)
col_ink = RGBf(0xe8/255, 0xef/255, 0xec/255)
col_dim = RGBf(0x9d/255, 0xb3/255, 0xab/255)
col_bq = RGBf(0xe5/255, 0x84/255, 0x68/255)
col_nk = RGBf(0x3e/255, 0xcf/255, 0xa2/255)
col_gold = RGBf(0xf0/255, 0xb4/255, 0x29/255)

set_theme!(Theme(
    backgroundcolor=col_bg, textcolor=col_ink, fontsize=17,
    Axis=(backgroundcolor=col_bg, xgridcolor=(:white, 0.08), ygridcolor=(:white, 0.0),
          xtickcolor=col_dim, ytickcolor=col_dim, leftspinecolor=col_dim, bottomspinecolor=col_dim,
          xlabelcolor=col_ink, ylabelcolor=col_ink, xticklabelcolor=col_dim, yticklabelcolor=col_dim,
          titlecolor=col_ink, topspinevisible=false, rightspinevisible=false),
))

fig = Figure(size=(1200, 480))
ax = Axis(fig[1, 1], xscale=log10, yreversed=true,
    yticks=(1:4, labels), xlabel="CPU-hours, log scale",
    title="Checking one peptide list against all of GTEx")
barplot!(ax, 1:4, cpuh, direction=:x, fillto=1e-5, color=[col_bq, col_bq, col_gold, col_nk])
for (y, v, s) in zip(1:4, cpuh, txt)
    text!(ax, v * 1.6, y, text=s, align=(:left, :center), color=col_ink, fontsize=16)
end
xlims!(ax, 1e-5, 2e5)
save(joinpath(@__DIR__, "cost.svg"), fig)
println("wrote cost.svg")
