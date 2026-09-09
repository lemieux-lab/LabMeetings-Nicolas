# Demo for the "Watching runtime compilation" slide.
#
#   julia --trace-compile=stderr script.jl
#   julia --trace-compile=stderr --trace-compile-timing script.jl
#
# Every precompile(...) line printed to stderr is a method instance Julia had to
# compile at runtime because nothing in the sysimage covered it. This is the raw
# material for a precompile directive or a PrecompileTools workload.
#
# Dependency-free on purpose, so it runs in any Julia.

struct Point
    x::Float64
    y::Float64
end

dist(a::Point, b::Point) = hypot(a.x - b.x, a.y - b.y)

function nearest(p::Point, pts::Vector{Point})
    best = first(pts)
    bd = dist(p, best)
    for q in pts
        d = dist(p, q)
        if d < bd
            bd = d
            best = q
        end
    end
    return best
end

pts = [Point(rand(), rand()) for _ in 1:1000]
origin = Point(0.0, 0.0)

println(nearest(origin, pts))
println(sum(dist(origin, q) for q in pts))

# A different set of types: substring keys, dict counting, a sort by value.
words = split("the quick brown fox jumps over the lazy dog the fox the dog")
freq = Dict{SubString{String}, Int}()
for w in words
    freq[w] = get(freq, w, 0) + 1
end
println(sort(collect(freq); by = last, rev = true))
