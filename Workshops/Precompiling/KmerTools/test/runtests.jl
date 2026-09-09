using KmerTools
using Test

@testset "kmer_count" begin
    c = kmer_count("ACDACD", 3)
    @test c["ACD"] == 2
    @test c["CDA"] == 1
    @test c["DAC"] == 1
    @test sum(values(c)) == 4
end

@testset "edge cases" begin
    @test kmer_count("AAAA", 1) == Dict("A" => 4)
    @test length(kmer_count("ACGT", 4)) == 1
    @test_throws ArgumentError kmer_count("AC", 5)
    @test_throws ArgumentError kmer_count("ACGT", 0)
end
