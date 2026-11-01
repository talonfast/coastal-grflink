from cargo import Cargo

cargo = Cargo(
    id="aircraft",
    type_name="string(STR_CARGO_NAME_AIRCRAFT)",
    unit_name="string(STR_CARGO_NAME_AIRCRAFT)",
    type_abbreviation="string(STR_CID_AIRCRAFT)",
    sprite="NEW_CARGO_SPRITE",
    weight="1.0",
    is_freight="1",
    cargo_classes = ['CC_PIECE_GOODS', 'CC_FLATBED', 'CC_NON_POTABLE'],
    cargo_label="ACFT",
    units_of_cargo="TTD_STR_TONS",
    items_of_cargo="string(STR_CARGO_UNIT_AIRCRAFT)",
    penalty_lowerbound="10",
    single_penalty_length="128",
    capacity_multiplier="1",
    price_factor=200,
    icon_indices=(15, 2),  # FIRS PNW: borrowed slot of an unregistered FIRS cargo
    sprites_complete=True,
)
