import Universality.Arithmetic.Section4
import Lean.Elab.Command
import Lean.Util.CollectAxioms

/-!
This is a verification tool, not a mathematical premise. The command checks
the kernel-recorded dependencies of every imported declaration whose source
module belongs to the Universality project. Selection uses module provenance,
including project declarations in other namespaces and generated declarations.

The final audit root must invoke the command explicitly: importing a compiled
copy of this file alone does not rerun a command executed during elaboration.
-/

open Lean Elab Command in
elab "#audit_section4_axioms" : command => do
  let environment ← getEnv
  let approved : Array Name := #[
    ``propext, ``Classical.choice, ``Quot.sound,
    ``Universality.External.six_exponentials,
    ``Universality.External.gelfond_schneider_real]
  let mut checkedDeclarations : Nat := 0
  let mut checkedModules : Nat := 0
  let mut codegenOnlyEntries : Nat := 0
  for sourceModule in environment.header.moduleNames do
    if (`Universality).isPrefixOf sourceModule then
      checkedModules := checkedModules + 1
  -- The effective origin map also contains code-generator-only auxiliary entries
  -- absent from the kernel (see Kernel.Environment.const2ModIdx's documentation).
  -- Intersecting with the checked environment selects the actual declarations.
  for (declarationName, originIndex) in environment.const2ModIdx.toList do
    let sourceModule := environment.header.moduleNames[originIndex]!
    if (`Universality).isPrefixOf sourceModule then
      if (environment.checked.get.find? declarationName).isSome then
        let dependencies ← Lean.collectAxioms declarationName
        for dependency in dependencies do
          unless approved.contains dependency do
            throwError "Unapproved dependency {dependency} in {declarationName}, source module {sourceModule}"
        checkedDeclarations := checkedDeclarations + 1
      else
        codegenOnlyEntries := codegenOnlyEntries + 1
  if checkedDeclarations == 0 || checkedModules == 0 then
    throwError "The Section 4 project declaration audit was empty"
  logInfo m!"SECTION4_KERNEL_AXIOM_AUDIT_OK declarations={checkedDeclarations} modules={checkedModules} codegenOnly={codegenOnlyEntries}"

#audit_section4_axioms
