# Bar chart, log scale: how big the GTEx table would be stored three ways.
# Derived from the real build (62,563,538,826 k-mers, 2,486 samples, 909,720,444,747 pairs,
# file size 2,361,372,418,996 bytes):
#   full grid, one 4-byte count per (k-mer, sample) cell: 62.56e9 x 2486 x 4 B = 622 TB
#   plain lists, 8-byte k-mer + each pair as two 4-byte numbers: (62.56e9 + 909.7e9) x 8 B = 7.78 TB
#   NeoKCT file as built: 2.36 TB (2.15 TiB)
#   memory line: oni, 1.875 TB of RAM
# Writes two versions: data_scale.svg (the problem, no NeoKCT bar) and storage.svg (with it).
# Run: julia --project=<LabMeetings root> plot_storage.jl

using CairoMakie

col_bg = RGBf(0x15/255, 0x1f/255, 0x1b/255)
col_ink = RGBf(0xe8/255, 0xef/255, 0xec/255)
col_dim = RGBf(0x9d/255, 0xb3/255, 0xab/255)
col_bad = RGBf(0xe5/255, 0x84/255, 0x68/255)
col_mid = RGBf(0x3e/255, 0xcf/255, 0xa2/255)
col_gold = RGBf(0xf0/255, 0xb4/255, 0x29/255)

set_theme!(Theme(
    backgroundcolor=col_bg, textcolor=col_ink, fontsize=17,
    Axis=(backgroundcolor=col_bg, xgridcolor=(:white, 0.08), ygridcolor=(:white, 0.0),
          xtickcolor=col_dim, ytickcolor=col_dim, leftspinecolor=col_dim, bottomspinecolor=col_dim,
          xlabelcolor=col_ink, ylabelcolor=col_ink, xticklabelcolor=col_dim, yticklabelcolor=col_dim,
          titlecolor=col_ink, topspinevisible=false, rightspinevisible=false),
))

labels = ["Full grid\n(every fragment × every sample)", "Lists, plain numbers\n(only present samples)", "NeoKCT\n(lists, packed and delta-encoded)"]
tb = [622.13, 7.78, 2.36]
txt = ["622 TB", "7.8 TB", "2.4 TB"]
ram = 1.875

function storage_plot(n, title, out)
    fig = Figure(size=(1200, 120 + 100n))
    ax = Axis(fig[1, 1], xscale=log10, yreversed=true, yticks=(1:n, labels[1:n]),
        xlabel="terabytes, log scale", title=title)
    barplot!(ax, 1:n, tb[1:n], direction=:x, fillto=0.5, color=[col_bad, col_bad, col_mid][1:n])
    for (y, v, s) in zip(1:n, tb[1:n], txt[1:n])
        text!(ax, v * 1.3, y, text=s, align=(:left, :center), color=col_ink, fontsize=17)
    end
    vlines!(ax, [ram], color=col_dim, linestyle=:dash, linewidth=2)
    text!(ax, ram * 1.08, 0.12, text="memory of our largest server, 1.9 TB", align=(:left, :center), color=col_dim, fontsize=15)
    xlims!(ax, 0.5, 5000)
    ylims!(ax, n + 0.5, -0.15)
    save(joinpath(@__DIR__, out), fig)
    println("wrote ", out)
end

storage_plot(2, "Holding every count for GTEx", "data_scale.svg")
storage_plot(3, "The GTEx table, stored three ways", "storage.svg")
