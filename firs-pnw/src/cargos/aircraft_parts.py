from cargo import Cargo

cargo = Cargo(
    id="aircraft_parts",
    type_name="string(STR_CARGO_NAME_AIRCRAFT_PARTS)",
    unit_name="string(STR_CARGO_NAME_AIRCRAFT_PARTS)",
    type_abbreviation="string(STR_CID_AIRCRAFT_PARTS)",
    sprite="NEW_CARGO_SPRITE",
    weight="1.0",
    is_freight="1",
    cargo_classes = ['CC_PIECE_GOODS', 'CC_NON_POTABLE'],
    cargo_label="ACPT",
    units_of_cargo="TTD_STR_TONS",
    items_of_cargo="string(STR_CARGO_UNIT_AIRCRAFT_PARTS)",
    penalty_lowerbound="7",
    single_penalty_length="255",
    capacity_multiplier="1",
    price_factor=160,
    icon_indices=(14, 2),  # FIRS PNW: borrowed slot of an unregistered FIRS cargo
    sprites_complete=True,
)
