module KmerTools

export kmer_count

"""
    kmer_count(seq::AbstractString, k::Int) -> Dict{String, Int}

Count every contiguous k-mer of length `k` in `seq`.

# Examples
julia> kmer_count("ACDACD", 3)
Dict("ACD" => 2, "CDA" => 1, "DAC" => 1)
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

# Live exercise: this module ships with no precompile setup on purpose.
# See solution.jl for the PrecompileTools version you build in step 3.

end # module
