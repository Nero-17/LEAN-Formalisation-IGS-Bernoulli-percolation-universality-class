"""Parse a completed full-declaration audit; never runs Lean or supplies proofs."""
from pathlib import Path
import argparse
import hashlib
import json

STANDARD = {"propext", "Classical.choice", "Quot.sound"}
GS = "Universality.External.gelfond_schneider_real"
REQUIRED_MODULES = {
    "Universality.Section5.SeedCertificates", "Universality.Section5.CertifiedConsequences",
    "Universality.Section5.PhysicalExponents", "Universality.Section5.ClassFourExponentials",
}
# Explicit mathematical endpoints, not a blanket allowance for any theorem
# whose name happens to contain 'transcendental'. Generated descendants are
# retained with the endpoint. Unexpected dependencies require human review.
GS_ENDPOINTS = {
    GS,
    "Universality.Section4.logarithmic_dimension_transcendental",
    "Universality.Section5.shifted_log_ratio_transcendental",
    "Universality.Section5.shifted_dimension_transcendental",
    "Universality.Section5.shifted_three_dimensions_transcendental",
    "Universality.Section5.ExactAllocationCertificate.shifted_dimensions_transcendental",
    "Universality.Section5.ExactAllocationCertificate.shifted_hausdorff_dimension_transcendental",
    "Universality.Section5.certifiedRuleShifted19_transcendental_dimensions",
    "Universality.Section5.certifiedRuleShifted19_hausdorff_dimension_transcendental",
    "Universality.Rule.Classical.criticalDimension_transcendental_of_irrational",
}


def parse(log, exit_code):
    if exit_code != 0:
        raise ValueError("Lean did not exit successfully")
    rows, modules, summaries = [], [], []
    with log.open(encoding="utf-8-sig") as stream:
        for line in stream:
            if line.startswith("SECTION5_AXIOM_ROW "):
                rows.append(json.loads(line.removeprefix("SECTION5_AXIOM_ROW ")))
            elif line.startswith("SECTION5_AXIOM_MODULE "):
                modules.append(line.removeprefix("SECTION5_AXIOM_MODULE ").strip())
            elif line.startswith("SECTION5_FINAL_KERNEL_AUDIT_OK "):
                summaries.append(json.loads(line.removeprefix("SECTION5_FINAL_KERNEL_AUDIT_OK ")))
    if len(summaries) != 1:
        raise ValueError("Expected exactly one completed audit marker")
    summary = summaries[0]
    if not rows or len(rows) != summary["declarations"] or len(modules) != summary["modules"]:
        raise ValueError("Incomplete declaration/module audit output")
    if len({row["declaration"] for row in rows}) != len(rows) or len(set(modules)) != len(modules):
        raise ValueError("Duplicate declaration/module audit entries")
    if not REQUIRED_MODULES.issubset(modules):
        raise ValueError("Final seed/physical/four-exponentials module coverage is incomplete")
    gs_rows, unexpected = [], []
    for row in rows:
        if row["module"] not in modules:
            raise ValueError("Declaration has an unlisted source module")
        if set(row["axioms"]) - (STANDARD | {GS}):
            raise ValueError(f"Unapproved axiom: {row}")
        if GS in row["axioms"]:
            gs_rows.append(row)
            name = row["declaration"]
            if not any(name == endpoint or name.startswith(endpoint + ".") for endpoint in GS_ENDPOINTS):
                unexpected.append(row)
    if len(gs_rows) != summary["gelfond_schneider_declarations"]:
        raise ValueError("Gelfond--Schneider count mismatch")
    digest = hashlib.sha256()
    with log.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"status": "dependency_audit_pass" if not unexpected else "unexpected_gs_dependency_requires_review",
            "lean_exit_code": exit_code, "log_sha256": digest.hexdigest(), **summary,
            "project_modules": sorted(modules), "gelfond_schneider_dependencies": gs_rows,
            "unexpected_gelfond_schneider_dependencies": unexpected,
            "scope": "Kernel-recorded dependencies of every imported project declaration. Source/object closure verification and mathematical review are separate; this script is not a proof."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    parser.add_argument("--exit-code", type=int, required=True, help="Actual compiler exit code")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = parse(args.log, args.exit_code)
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    raise SystemExit(0 if result["status"] == "dependency_audit_pass" else 1)
