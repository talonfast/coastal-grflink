from cargo import Cargo

cargo = Cargo(
    id="ships",
    type_name="string(STR_CARGO_NAME_SHIPS)",
    unit_name="string(STR_CARGO_NAME_SHIPS)",
    type_abbreviation="string(STR_CID_SHIPS)",
    sprite="NEW_CARGO_SPRITE",
    weight="1.0",
    is_freight="1",
    cargo_classes = ['CC_PIECE_GOODS', 'CC_FLATBED', 'CC_NON_POTABLE'],
    cargo_label="SHIP",
    units_of_cargo="TTD_STR_TONS",
    items_of_cargo="string(STR_CARGO_UNIT_SHIPS)",
    penalty_lowerbound="14",
    single_penalty_length="255",
    capacity_multiplier="1",
    price_factor=190,
    icon_indices=(14, 5),  # FIRS PNW: borrowed slot of an unregistered FIRS cargo
    sprites_complete=True,
)
