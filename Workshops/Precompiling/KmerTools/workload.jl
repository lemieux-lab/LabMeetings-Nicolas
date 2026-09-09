# A representative run of KmerTools, used for the stretch goal.
#
#   using SnoopCompileCore
#   tinf = @snoop_inference begin include("workload.jl") end
#   using SnoopCompile
#   display(tinf)                 # inference flame data
#   itrigs = inference_triggers(tinf)
#
# Add the calls behind the most expensive inference roots to @compile_workload
# in solution.jl, then re-measure.

using KmerTools

for seq in ("ACDEFGHIKLMNPQRSTVWY"^10, "ACGT"^100, "MKTAYIAKQR"^30)
    for k in (2, 3, 4, 6, 9)
        kmer_count(seq, k)
    end
end
