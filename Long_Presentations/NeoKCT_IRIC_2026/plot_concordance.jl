# Scatter for "Does it agree with BamQuery?": every (peptide, sample) pair, BamQuery rphm vs.
# NeoKCT rphm, 22 thymic samples x 351 peptides BamQuery could place = 7,722 pairs.
# Data: c5_pairs_ds.tsv from export_c5_pairs.py, same join as the paper's C5_concordance_ds_suffix.py
# (suffix-anchored peptide queries: Spearman 0.939, log-log slope 0.992 on single-origin pairs).
#
# Log axes can't show zeros, and zeros are most of the data (6,947 pairs are 0 in both tools),
# so zeros get their own strip below/left of the log range instead of being dropped or log1p'd.
# Smallest non-zero value is ~1.1 rphm (one read), so the log range starts at 1.
# Run: julia --project=<LabMeetings root> plot_concordance.jl

using CairoMakie

## Load ##

bq = Float64[]; nk = Float64[]; multi = Bool[]
for (i, line) in enumerate(eachline(joinpath(@__DIR__, "c5_pairs_ds.tsv")))
    i == 1 && continue
    f = split(line, '\t')
    push!(bq, parse(Float64, f[7])); push!(nk, parse(Float64, f[8])); push!(multi, parse(Int, f[4]) > 1)
end
length(bq) == 7722 || error("expected 7722 pairs, got $(length(bq))")

const ZERO = -0.5  # where a zero count sits on the log10 axis
pos(v) = v > 0 ? log10(v) : ZERO
x = pos.(bq); y = pos.(nk)
both_zero = (bq .== 0) .& (nk .== 0)
n_both_zero = count(both_zero)

## Style ##

col_bg = RGBf(0x15/255, 0x1f/255, 0x1b/255)
col_ink = RGBf(0xe8/255, 0xef/255, 0xec/255)
col_dim = RGBf(0x9d/255, 0xb3/255, 0xab/255)
col_single = RGBf(0x3e/255, 0xcf/255, 0xa2/255)
col_multi = RGBf(0xf0/255, 0xb4/255, 0x29/255)
col_strip = RGBf(0x1c/255, 0x28/255, 0x22/255)

set_theme!(Theme(
    backgroundcolor=col_bg, textcolor=col_ink, fontsize=17,
    Axis=(backgroundcolor=col_bg, xgridcolor=(:white, 0.06), ygridcolor=(:white, 0.06),
          xtickcolor=col_dim, ytickcolor=col_dim, leftspinecolor=col_dim, bottomspinecolor=col_dim,
          xlabelcolor=col_ink, ylabelcolor=col_ink, xticklabelcolor=col_dim, yticklabelcolor=col_dim,
          titlecolor=col_ink, topspinevisible=false, rightspinevisible=false),
    Legend=(backgroundcolor=col_bg, framevisible=false, labelcolor=col_ink),
))

## Plot ##

ticks = ([ZERO, 0, 1, 2, 3], ["0", "1", "10", "100", "1,000"])
fig = Figure(size=(900, 800))
ax = Axis(fig[1, 1], xticks=ticks, yticks=ticks, aspect=DataAspect(),
    xlabel="BamQuery (reads per hundred million)", ylabel="NeoKCT (reads per hundred million)",
    title="7,722 (peptide, sample) pairs, 22 thymic samples")
lo, hi = ZERO - 0.25, 3.05
# zero strips, so the break between "0" and the log range reads as a break
poly!(ax, Rect2f(lo, lo, hi - lo, ZERO + 0.25 - lo), color=col_strip)
poly!(ax, Rect2f(lo, lo, ZERO + 0.25 - lo, hi - lo), color=col_strip)
lines!(ax, [0, hi], [0, hi], color=col_dim, linestyle=:dash, linewidth=1.5)
text!(ax, 2.55, 2.75, text="same count", color=col_dim, fontsize=14, rotation=π/4, align=(:center, :bottom))
# multi-origin first so the single-origin points stay visible on top
for (m, c, lab) in ((multi, col_multi, "several genomic origins"), (.!multi, col_single, "one genomic origin"))
    sel = m .& .!both_zero
    scatter!(ax, x[sel], y[sel], color=(c, 0.55), markersize=8, strokewidth=0, label=lab)
end
scatter!(ax, [ZERO], [ZERO], color=col_dim, markersize=22)
text!(ax, ZERO + 0.12, ZERO + 0.1, text="$(replace(string(n_both_zero), r"(\d)(\d{3})$" => s"\1,\2")) pairs: zero in both",
      color=col_dim, fontsize=14, align=(:left, :bottom))
xlims!(ax, lo, hi); ylims!(ax, lo, hi)
Legend(fig[2, 1], ax, orientation=:horizontal, markersize=14, tellheight=true)
save(joinpath(@__DIR__, "concordance.svg"), fig)
println("wrote concordance.svg: $(length(bq)) pairs, $n_both_zero zero in both")
