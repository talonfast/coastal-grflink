"""
Checks for the Pacific Northwest economy, run with: python src/check_pnw.py
Loads FIRS's own registries (firs.main) and exits non-zero listing every failure.
"""

import sys

import firs

ECONOMY = "PACIFIC_NORTHWEST"
TOWN_CARGOS = {"PASS", "MAIL"}  # produced and accepted by towns, not industries
SUPPLY_CARGOS = {"ENSP", "FMSP", "JETF"}  # boost primaries; nothing needs to produce them for the chain to work
NEW_CARGO_LABELS = ["ACPT", "ALUM", "ACFT", "ACFC", "FLPL", "SHIP", "JETF", "PODY", "EGSW"]
MAX_CARGOS = 64  # cargo types per GRF
# placed only in the scenario editor at their real sites; never spawn, never close, players cannot fund them
SCENARIO_ONLY = ["dreamlifter_delivery_airport", "aluminium_smelter", "aircraft_assembly_plant", "aircraft_qa_centre",
                 "customer_acceptance_centre", "floatplane_factory", "seaplane_base", "oil_terminal"]


def main():
    firs.main()
    failures = []
    economy = firs.economy_manager.get_economy_by_id(ECONOMY)
    if economy is None:
        print(f"FAIL: economy {ECONOMY} is not registered")
        return 1

    labels_by_id = {cargo.id: cargo.cargo_label for cargo in firs.cargo_manager}
    economy_labels = {labels_by_id[c] for c in economy.cargo_ids if c in labels_by_id}
    missing_modules = [c for c in economy.cargo_ids if c not in labels_by_id]
    if missing_modules:
        failures.append(f"economy cargos without a registered cargo module: {missing_modules}")

    produced, accepted = {}, {}
    for industry in firs.industry_manager:
        if not industry.economy_variations[ECONOMY].enabled:
            continue
        for label, _ in industry.get_prod_cargo_types(economy):
            produced.setdefault(label, []).append(industry.id)
        for label in industry.get_accepted_cargo_labels_by_economy(economy):
            accepted.setdefault(label, []).append(industry.id)

    for label, by in sorted(produced.items()):
        if label not in accepted and label not in TOWN_CARGOS:
            failures.append(f"{label} is produced by {by} but nothing accepts it")
    for label, by in sorted(accepted.items()):
        if label not in produced and label not in SUPPLY_CARGOS | TOWN_CARGOS:
            failures.append(f"{label} is accepted by {by} but nothing produces it")
    for label in sorted(set(produced) | set(accepted)):
        if label not in economy_labels:
            failures.append(f"{label} is used by industries but not in the economy's cargo list")
    for label in NEW_CARGO_LABELS:
        if label not in produced and label not in SUPPLY_CARGOS:
            failures.append(f"new cargo {label} has no producer")
        if label not in accepted:
            failures.append(f"new cargo {label} has no consumer")

    all_labels = [cargo.cargo_label for cargo in firs.cargo_manager]
    for label in NEW_CARGO_LABELS:
        if label not in all_labels:
            failures.append(f"new cargo {label} is not registered")
    dupes = {label for label in all_labels if all_labels.count(label) > 1}
    if dupes:
        failures.append(f"duplicate cargo labels: {sorted(dupes)}")
    if len(all_labels) > MAX_CARGOS:
        failures.append(f"{len(all_labels)} cargos registered, the limit is {MAX_CARGOS}")

    ids = {industry.id: industry for industry in firs.industry_manager}
    for industry_id in SCENARIO_ONLY:
        industry = ids.get(industry_id)
        if industry is None:
            failures.append(f"scenario-only industry {industry_id} is not registered")
            continue
        if not getattr(industry, "scenario_only", False):
            failures.append(f"{industry_id} is not marked scenario_only")
        for prop in ("prob_map_gen", "prob_in_game"):
            if str(industry.get_property(prop, economy)) != "0":
                failures.append(f"{industry_id} {prop} is not 0")
        # the engine abandons processing industries without a production-change callback; black holes are exempt
        if industry.template == "industry_tertiary.pynml" and industry.get_property("life_type", economy) != "IND_LIFE_TYPE_BLACK_HOLE":
            failures.append(f"{industry_id} is a tertiary without black-hole life type")

        # the editor places these at real sites, which the tile checks must not refuse (founder bypass)
        for tile in industry.tiles:
            checks = getattr(tile, "location_checks", None)
            if checks is not None and hasattr(checks, "always_allow_founder") and not checks.always_allow_founder:
                failures.append(f"{industry_id} tile {tile.id} refuses editor placement (always_allow_founder off)")

    # counted in items, a 15 t aircraft would pay like one crate of goods; count everything by weight or volume
    for cargo in firs.cargo_manager:
        if cargo.cargo_label in NEW_CARGO_LABELS and cargo.units_of_cargo == "TTD_STR_ITEMS":
            failures.append(f"new cargo {cargo.cargo_label} is counted in items")

    for f in failures:
        print("FAIL:", f)
    print(f"{len(failures)} failures; {len(produced)} cargos produced, {len(accepted)} accepted, {len(all_labels)} registered")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
