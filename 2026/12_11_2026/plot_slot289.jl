# Bar chart: distinct k-mers counted for sample SRR614719 (table slot 289).
# All three numbers are measured: the single-strand build, the original double-strand
# build (the glitch), and the fresh independent recount of the same CRAM that was used
# for the patch. Source: PAPER_TODO.md C11.
# Run: julia --project=<LabMeetings root> plot_slot289.jl

using CairoMakie

labels = ["Single-strand\nbuild", "Double-strand\nbuild (glitch)", "Double-strand\nrecount"]
kmers_m = [209.495955, 28.118763, 335.450762]  # millions of distinct k-mers

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
    ylabel="distinct k-mers counted (millions)",
    title="SRR614719 (artery_tibial), same CRAM, three counts")

barplot!(ax, 1:3, kmers_m, width=0.55, color=[col_ok, col_bad, col_ok])
for (i, v) in enumerate(kmers_m)
    text!(ax, i, v + 8, text=string(round(v, digits=1), " M"), align=(:center, :bottom), color=col_ink, fontsize=16)
end
ylims!(ax, 0, 390)

out_path = joinpath(@__DIR__, "slot289_counts.svg")
save(out_path, fig)
println("wrote ", out_path)
