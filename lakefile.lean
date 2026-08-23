import Lake
open Lake DSL

package «erdosstraussolver» where

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.28.0"

@[default_target]
lean_lib «ErdosStraus» where
  -- root is ErdosStraus.lean or ErdosStraus/Basic.lean
