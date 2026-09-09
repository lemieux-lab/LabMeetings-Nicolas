# KmerTools

Toy package for the precompilation workshop live exercise. One exported
function, `kmer_count`, and no precompile setup to start with. The exercise is
to measure its time to first call, add a `PrecompileTools` workload, and measure
again.

## Layout

- `src/KmerTools.jl` : the starting point, no precompile directives
- `solution.jl` : the finished version with a `@compile_workload`
- `workload.jl` : a longer representative run for the stretch goal
- `test/runtests.jl` : a small test set

## Setup

From this directory:

```
import Pkg
Pkg.activate(".")
Pkg.instantiate()   # nothing to fetch yet, the base package has no deps
```

## Step 1: count what compiles at runtime

```
julia --project=. --trace-compile=stderr -e 'using KmerTools; kmer_count("ACDACDACD", 3)'
```

Every printed `precompile(...)` line is a method the cache did not cover. Count
them.

## Step 2: see the import cost

```
julia --project=. -e 'using InteractiveUtils; @time_imports using KmerTools'
```

Note the compilation percentage next to `KmerTools`.

## Step 3: add a workload

```
Pkg.activate(".")
Pkg.add("PrecompileTools")
```

Copy `solution.jl` over `src/KmerTools.jl`. That adds:

```julia
@setup_workload begin
    example = "ACDEFGHIKLMNPQRSTVWY"^5
    @compile_workload begin
        kmer_count(example, 3)
        kmer_count(example, 6)
        kmer_count("ACGT"^20, 4)
    end
end
```

## Step 4: measure again

Restart Julia so precompilation reruns, then repeat steps 1 and 2. The
runtime-compiled list should be shorter and the import should spend more time
loading and less compiling.

## Stretch: derive the workload from evidence

```julia
using SnoopCompileCore
tinf = @snoop_inference begin include("workload.jl") end
using SnoopCompile
display(tinf)
```

Add the calls behind the most expensive inference roots to the
`@compile_workload` block, then measure once more.

## Tests

```
Pkg.test("KmerTools")
```
