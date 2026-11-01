from cargo import Cargo

cargo = Cargo(
    id="floatplanes",
    type_name="string(STR_CARGO_NAME_FLOATPLANES)",
    unit_name="string(STR_CARGO_NAME_FLOATPLANES)",
    type_abbreviation="string(STR_CID_FLOATPLANES)",
    sprite="NEW_CARGO_SPRITE",
    weight="1.0",
    is_freight="1",
    cargo_classes = ['CC_PIECE_GOODS', 'CC_FLATBED', 'CC_NON_POTABLE'],
    cargo_label="FLPL",
    units_of_cargo="TTD_STR_TONS",
    items_of_cargo="string(STR_CARGO_UNIT_FLOATPLANES)",
    penalty_lowerbound="10",
    single_penalty_length="128",
    capacity_multiplier="1",
    price_factor=210,
    icon_indices=(9, 4),  # FIRS PNW: borrowed slot of an unregistered FIRS cargo
    sprites_complete=True,
)
