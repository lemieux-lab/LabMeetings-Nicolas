# Demo for the "World age" slides. Run it line by line in the REPL, or all at
# once with:  julia world_age.jl
#
# Shows the world counter moving, a CodeInstance being capped through a
# backedge, and the world age barrier.

print_ci(f) = for m in methods(f), mi in Base.specializations(m)
    mi === nothing && continue
    c = mi.cache
    while true
        println("  ", f, "  min_world=", c.min_world, "  max_world=", c.max_world,
                c.max_world == typemax(UInt) ? "  (live)" : "  (dead)")
        isdefined(c, :next) && c.next !== nothing ? (c = c.next) : break
    end
end

## 1. the counter moves on every method definition

println("counter: ", Base.get_world_counter())
inner(x) = x + 1
outer(x) = inner(x)
println("counter: ", Base.get_world_counter(), "  after defining inner, outer")

## 2. a CodeInstance is born, then capped through its backedge

outer(1)
println("counter: ", Base.get_world_counter(), "  after first outer(1)")
print_ci(outer)

Core.eval(@__MODULE__, :(inner(x) = x + 100))
println("counter: ", Base.get_world_counter(), "  after redefining inner")
print_ci(outer)   # the old CodeInstance now has a finite max_world

outer(1)
println("counter: ", Base.get_world_counter(), "  after second outer(1)")
print_ci(outer)   # a fresh live CodeInstance, the dead one still hangs in the chain

## 3. the world age barrier

val() = 1
function barrier()
    a = val()
    Core.eval(@__MODULE__, :(val() = 2))
    b = val()                    # still 1: this frame is pinned to the old world
    c = Base.invokelatest(val)   # 2: the current world
    println("  (a, b, c) = ", (a, b, c))
end
barrier()
println("  val() at top level = ", val())

# The louder version: a function whose only method is defined mid-run throws
# "MethodError: method too new to be called from this world context".
# On Julia 1.12 that pattern also prints a global-binding deprecation warning,
# so the quiet (1, 1, 2) demo above is the stable one.
