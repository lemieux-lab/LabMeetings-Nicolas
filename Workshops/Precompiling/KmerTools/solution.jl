# Reference solution for step 3 of the live exercise.
#
# After running, from inside this package environment:
#   import Pkg; Pkg.activate("."); Pkg.add("PrecompileTools")
# copy this file over src/KmerTools.jl, then restart Julia and re-measure.

module KmerTools

using PrecompileTools

export kmer_count

"""
    kmer_count(seq::AbstractString, k::Int) -> Dict{String, Int}

Count every contiguous k-mer of length `k` in `seq`.
"""
function kmer_count(seq::AbstractString, k::Int)
    1 <= k <= length(seq) || throw(ArgumentError("need 1 <= k <= length(seq), got k=$k for a length $(length(seq)) sequence"))
    counts = Dict{String, Int}()
    for i in 1:(length(seq) - k + 1)
        mer = seq[i:i+k-1]
        counts[mer] = get(counts, mer, 0) + 1
    end
    return counts
end

# Runs during precompilation. Every method reached here is inferred, compiled,
# and stored in the pkgimage, so the first real call in a fresh session is fast.
@setup_workload begin
    example = "ACDEFGHIKLMNPQRSTVWY"^5
    @compile_workload begin
        kmer_count(example, 3)
        kmer_count(example, 6)
        kmer_count("ACGT"^20, 4)
    end
end

end # module
