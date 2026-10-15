# Horizontal bar chart: the 103 published ovarian aeTSA/mTSA candidates (Zhao et al. 2020),
# broken down by which validation criteria they meet against the C8 tumor cohort + C9/GTEx references.
# These categories overlap (not a strict funnel), so each bar is read independently as n/103.
# Run: julia --project=<LabMeetings root> plot_candidate_breakdown.jl

using CairoMakie

labels = [
    "No RNA support in any tumor sample",
    "Meets published 2x TAA criterion",
    "Dual-reference specific AND tumor-detected",
    "Specific against both GTEx and DC/mTEC",
    "RNA-level support in own tumor",
]
counts = [12, 8, 29, 38, 91]
pct = round.(counts ./ 103 .* 100, digits=1)

col_bg = RGBf(0x15/255, 0x1f/255, 0x1b/255)
col_ink = RGBf(0xe8/255, 0xef/255, 0xec/255)
col_dim = RGBf(0x9d/255, 0xb3/255, 0xab/255)
col_bar = RGBf(0x3e/255, 0xcf/255, 0xa2/255)
col_warn = RGBf(0xe5/255, 0x84/255, 0x68/255)
col_gold = RGBf(0xf0/255, 0xb4/255, 0x29/255)

set_theme!(Theme(
    backgroundcolor=col_bg,
    textcolor=col_ink,
    Axis=(backgroundcolor=col_bg, xgridcolor=(:white, 0.06), ygridcolor=(:white, 0.0),
          xtickcolor=col_dim, ytickcolor=col_dim, leftspinecolor=col_dim, bottomspinecolor=col_dim,
          xlabelcolor=col_ink, ylabelcolor=col_ink, xticklabelcolor=col_dim, yticklabelcolor=col_dim,
          titlecolor=col_ink),
))

fig = Figure(size=(1040, 440))
ax = Axis(fig[1, 1],
    yticks=(1:length(labels), labels),
    xlabel="/ 103 candidates",
    title="103 published ovarian aeTSA/mTSA candidates (Zhao et al. 2020), by criterion")

colors = [i == 1 ? col_warn : i == 3 ? col_gold : col_bar for i in 1:length(labels)]
barplot!(ax, 1:length(labels), counts, direction=:x, color=colors)

for (y, n, p) in zip(1:length(labels), counts, pct)
    label_color = y == 3 ? col_gold : col_ink
    text!(ax, n + 2, y, text="$(n)/103 ($(p)%)", align=(:left, :center), color=label_color, fontsize=15)
end

xlims!(ax, 0, 103)
out_path = joinpath(@__DIR__, "candidate_breakdown.svg")
save(out_path, fig)
println("wrote ", out_path)
