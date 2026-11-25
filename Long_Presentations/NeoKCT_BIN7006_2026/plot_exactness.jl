# Two panels for "Approximate was never an option": true count (Jellyfish) vs. what each tool
# returns, every (k-mer, sample) pair of the paper's B4 benchmark (20,000 nucleotide 31-mers x 200
# GTEx samples), each tool against the truth that matches its own counting convention.
# NeoKCT's nucleotide mode counts forward-strand k-mers, so its truth is the forward Jellyfish
# count. REINDEER counts canonical k-mers (forward and reverse complement folded together, GTEx is
# unstranded), so its truth is forward + reverse-complement. The first version of this plot scored
# REINDEER against forward-only truth and charged it for every antisense read, see
# paper/scripts/B4_compute_accuracy_canonical.py. REINDEER's index also drops k-mers seen once in a
# sample (BCALM -abundance-min 2, its default), which is most of its zero strip.
# Data: B4_accuracy_canonical_per_pair.tsv. NeoKCT's faint red trail is the old build dropping
# N-containing reads, the slide notes 100% when they are kept (rebuild in preparation).
#
#=
Counts are small integers and most pairs share a handful of (true, reported) values, so 60k dots
would pile up into a few blobs that hide how many sit where. Pairs are aggregated instead, one
bubble per distinct (true, reported) with area proportional to the number of pairs, capped so the
biggest one doesn't swallow the panel. Zeros on either axis get their own strip outside the log
range, same trick as plot_concordance.jl.
=#
# Run: julia --project=<LabMeetings root> plot_exactness.jl

using CairoMakie

const DATA = "/u/jacquinn/phd_stuff/Manuscripts/NeoKCT/paper/results/B4_accuracy_canonical_per_pair.tsv"

## Load ##

nk = Dict{Tuple{Int,Int},Int}(); rd = Dict{Tuple{Int,Int},Int}()
n = 0
for (i, line) in enumerate(eachline(DATA))
    i == 1 && continue
    f = split(line, '\t')
    fwd, canon = parse(Int, f[5]), parse(Int, f[7])
    k_nk = (fwd, parse(Int, f[8])); k_rd = (canon, parse(Int, f[9]))
    nk[k_nk] = get(nk, k_nk, 0) + 1
    rd[k_rd] = get(rd, k_rd, 0) + 1
    global n += 1
end

const ZERO = -0.5  # where a reported zero sits on the log10 axis
pos(v) = v > 0 ? log10(v) : ZERO
fmt(x) = replace(string(x), r"(\d)(?=(\d{3})+$)" => s"\1,")

## Style ##

col_bg = RGBf(0x15/255, 0x1f/255, 0x1b/255)
col_ink = RGBf(0xe8/255, 0xef/255, 0xec/255)
col_dim = RGBf(0x9d/255, 0xb3/255, 0xab/255)
col_ok = RGBf(0x3e/255, 0xcf/255, 0xa2/255)
col_bad = RGBf(0xe5/255, 0x84/255, 0x68/255)
col_strip = RGBf(0x1c/255, 0x28/255, 0x22/255)

set_theme!(Theme(
    backgroundcolor=col_bg, textcolor=col_ink, fontsize=17,
    Axis=(backgroundcolor=col_bg, xgridcolor=(:white, 0.06), ygridcolor=(:white, 0.06),
          xtickcolor=col_dim, ytickcolor=col_dim, leftspinecolor=col_dim, bottomspinecolor=col_dim,
          xlabelcolor=col_ink, ylabelcolor=col_ink, xticklabelcolor=col_dim, yticklabelcolor=col_dim,
          titlecolor=col_ink, titlesize=20, topspinevisible=false, rightspinevisible=false),
))

## Plot ##

lo, hi = ZERO - 0.3, 3.35
ticks = ([ZERO, 0, 1, 2, 3], ["0", "1", "10", "100", "1,000"])
maxm = maximum(max(maximum(values(nk)), maximum(values(rd))))
fig = Figure(size=(1300, 620))
panels = (("NeoKCT", nk, "true count, forward strand (Jellyfish)"),
          ("REINDEER", rd, "true count, both strands (Jellyfish)"))
for (j, (name, d, xlab)) in enumerate(panels)
    ax = Axis(fig[1, j], title=name, xticks=ticks, yticks=ticks,
        aspect=DataAspect(), xlabel=xlab, ylabel=j == 1 ? "count returned" : "")
    poly!(ax, Rect2f(lo, lo, hi - lo, ZERO + 0.25 - lo), color=col_strip)
    poly!(ax, Rect2f(lo, lo, ZERO + 0.25 - lo, hi - lo), color=col_strip)
    lines!(ax, [0, hi], [0, hi], color=col_dim, linestyle=:dash, linewidth=1.2)
    keys_ = collect(keys(d))
    x = [pos(k[1]) for k in keys_]; y = [pos(k[2]) for k in keys_]
    m = [d[k] for k in keys_]
    exact = [k[1] == k[2] for k in keys_]
    # area proportional to pair count, floor so singletons stay visible
    sz = 4 .+ 44 .* sqrt.(m ./ maxm)
    for (sel, c) in ((.!exact, col_bad), (exact, col_ok))
        scatter!(ax, x[sel], y[sel], markersize=sz[sel], color=(c, 0.6), strokewidth=0)
    end
    missed = sum(v for (k, v) in d if k[1] > 0 && k[2] == 0; init=0)
    once = sum(v for (k, v) in d if k[1] == 1 && k[2] == 0; init=0)
    invented = sum(v for (k, v) in d if k[1] == 0 && k[2] > 0; init=0)
    # just above the zero strip, below the diagonal where no bubble can be
    lab = j == 2 ? "↓ $(fmt(missed)) present, returned 0\n   ($(fmt(once)) seen once, dropped by default)" :
                   "↓ $(fmt(missed)) present, returned 0"
    missed > 0 && text!(ax, 1.0, j == 2 ? -0.02 : -0.12, text=lab, color=col_bad, fontsize=15, align=(:left, :center))
    invented > 0 && text!(ax, ZERO + 0.22, 2.75, text="$(fmt(invented)) absent,\nreturned > 0",
                          color=col_bad, fontsize=15, align=(:left, :center))
    xlims!(ax, lo, hi); ylims!(ax, lo, hi)
end
save(joinpath(@__DIR__, "exactness.svg"), fig)
println("wrote exactness.svg: $n pairs, $(length(nk)) NeoKCT bubbles, $(length(rd)) REINDEER bubbles")
