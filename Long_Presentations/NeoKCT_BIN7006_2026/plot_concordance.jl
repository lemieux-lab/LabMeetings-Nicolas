# Scatter for "Does it agree with BamQuery?": every (peptide, sample) pair, BamQuery rphm vs.
# NeoKCT rphm, 22 thymic samples x 351 peptides BamQuery could place = 7,722 pairs. The 199
# peptides BamQuery couldn't place have no BamQuery value at all, so they get their own column
# left of the zero strip instead of pretending they're zeros: 4,378 pairs, 64 with NeoKCT reads.
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
nk_unplaced = Float64[]
for (i, line) in enumerate(eachline(joinpath(@__DIR__, "c5_pairs_ds.tsv")))
    i == 1 && continue
    f = split(line, '\t')
    f[7] == "NA" && (push!(nk_unplaced, parse(Float64, f[8])); continue)
    push!(bq, parse(Float64, f[7])); push!(nk, parse(Float64, f[8])); push!(multi, parse(Int, f[4]) > 1)
end
length(bq) == 7722 || error("expected 7722 placed pairs, got $(length(bq))")
length(nk_unplaced) == 4378 || error("expected 4378 unplaced pairs, got $(length(nk_unplaced))")

const ZERO = -0.5  # where a zero count sits on the log10 axis
const UNPLACED = -1.65  # x position of the "BamQuery couldn't place it" column
const HALF = 0.6  # half-width of that column, in log10 units
const SWARM_PX = 5.5  # marker size of the swarm points
const SWARM_D = 0.036  # one marker diameter in data units (~165 px per log10 unit at this figure size)

#=
Beeswarm placement: walk the points in value order and put each one at the free horizontal slot
closest to the centre line (0, +d, -d, +2d, ...), where free means no already placed point within
one diameter. Unlike binning by value this also handles values that are distinct but closer than a
marker, like the 0.36 to 0.39 pile here (one vs. two reads in slightly different libraries).
=#
function _swarm(y::AbstractVector{<:Real}, d::Real)
    xs = Float64[]
    for (i, yi) in enumerate(y)
        for k in 0:1000
            cand = iseven(k) ? (k ÷ 2) * d : -((k + 1) ÷ 2) * d
            any(j -> hypot(xs[j] - cand, y[j] - yi) < d, 1:i-1) && continue
            push!(xs, cand); break
        end
    end
    return xs
end
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
col_unplaced = RGBf(0xe5/255, 0x84/255, 0x68/255)

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
xticks = ([UNPLACED, ZERO, 0, 1, 2, 3], ["not\nplaced", "0", "1", "10", "100", "1,000"])
fig = Figure(size=(980, 800))
ax = Axis(fig[1, 1], xticks=xticks, yticks=ticks, aspect=DataAspect(),
    xlabel="BamQuery (reads per hundred million)", ylabel="NeoKCT (reads per hundred million)",
    title="550 peptides x 22 thymic samples")
lo, hi = ZERO - 0.25, 3.05
xlo = UNPLACED - HALF
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
# unplaced column: BamQuery has no value, NeoKCT still counts. Beeswarm so the x spread means
# "this many pairs at this level": counts are small integers, so many pairs share a value.
poly!(ax, Rect2f(xlo, lo, UNPLACED + HALF - xlo, hi - lo), color=(col_unplaced, 0.08))
up = nk_unplaced .> 0
yu = sort(log10.(nk_unplaced[up]))
xu = UNPLACED .+ _swarm(yu, SWARM_D)
maximum(abs, xu .- UNPLACED) < HALF || @warn "swarm wider than the column, raise HALF"
scatter!(ax, xu, yu, color=(col_unplaced, 0.8), markersize=SWARM_PX, strokewidth=0,
         label="BamQuery couldn't place (199 peptides)")
scatter!(ax, [UNPLACED], [ZERO], color=(col_unplaced, 0.75), markersize=22)
text!(ax, UNPLACED, ZERO - 0.13, text="$(replace(string(count(.!up)), r"(\d)(\d{3})$" => s"\1,\2"))",
      color=col_unplaced, fontsize=13, align=(:center, :top))
xlims!(ax, xlo, hi); ylims!(ax, lo, hi)
Legend(fig[2, 1], ax, orientation=:horizontal, markersize=14, tellheight=true)
save(joinpath(@__DIR__, "concordance.svg"), fig)
println("wrote concordance.svg: $(length(bq)) placed pairs, $n_both_zero zero in both, $(count(nk_unplaced .> 0)) unplaced pairs with reads")
