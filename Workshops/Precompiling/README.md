# Julia Precompilation workshop

Slides: `julia_precompiler_workshop.qmd` (Quarto revealjs). Render with
`quarto render julia_precompiler_workshop.qmd`.

## Environment

`Project.toml` and `Manifest.toml` in this folder pin everything the demos use:

- `CairoMakie` : the heavy-precompile example in Blocks 1 and 2
- `PrecompileTools` : `@compile_workload`, `@recompile_invalidations`
- `SnoopCompileCore` / `SnoopCompile` : `@snoop_invalidations`, `@snoop_inference`
- `JET` : `@report_opt` for inference problems
- `Cthulhu` : `@descend`
- `PackageCompiler` : `create_sysimage` in Block 5
- `InteractiveUtils` : `@time_imports`

Set it up once:

```
julia --project=. -e 'using Pkg; Pkg.instantiate()'
```

That first instantiate precompiles the whole stack, CairoMakie included, so it
takes a few minutes. That wait is the thing the workshop is about, so it is
worth watching with `--trace-compile` or `@time_imports` the first time.

Pinned to Julia 1.11 in `[compat]`. The manifest was resolved on 1.12, so an
older 1.11 will re-resolve on first use.

## Files

- `julia_precompiler_workshop.qmd` : the deck
- `script.jl` : trace-compile demo for the "Watching runtime compilation" slide
- `world_age.jl` : world counter, CodeInstance capping, and the barrier, for Block 3
- `KmerTools/` : the toy package for the Block 6 live exercise, with its own
  environment and a `README.md` walking through the four steps
