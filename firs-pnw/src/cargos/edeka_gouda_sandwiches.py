from cargo import Cargo

cargo = Cargo(
    id="edeka_gouda_sandwiches",
    type_name="string(STR_CARGO_NAME_EDEKA_GOUDA_SANDWICHES)",
    unit_name="string(STR_CARGO_NAME_EDEKA_GOUDA_SANDWICHES)",
    type_abbreviation="string(STR_CID_EDEKA_GOUDA_SANDWICHES)",
    sprite="NEW_CARGO_SPRITE",
    weight="1.0",
    is_freight="1",
    cargo_classes = ['CC_EXPRESS', 'CC_COVERED_BULK', 'CC_PIECE_GOODS', 'CC_LIQUID_BULK', 'CC_POTABLE', 'CC_REFRIGERATED'],
    cargo_label="EGSW",
    units_of_cargo="TTD_STR_TONS",
    items_of_cargo="string(STR_CARGO_UNIT_EDEKA_GOUDA_SANDWICHES)",
    penalty_lowerbound="0",
    single_penalty_length="20",
    capacity_multiplier="1",
    price_factor=175,
    icon_indices=(5, 0),  # FIRS PNW: borrowed slot of an unregistered FIRS cargo
    sprites_complete=True,
)
