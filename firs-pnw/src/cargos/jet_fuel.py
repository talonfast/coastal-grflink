from cargo import Cargo

cargo = Cargo(
    id="jet_fuel",
    type_name="string(STR_CARGO_NAME_JET_FUEL)",
    unit_name="string(STR_CARGO_NAME_JET_FUEL)",
    type_abbreviation="string(STR_CID_JET_FUEL)",
    sprite="NEW_CARGO_SPRITE",
    weight="0.8",
    is_freight="1",
    cargo_classes = ['CC_LIQUID_BULK', 'CC_NON_POTABLE'],
    cargo_label="JETF",
    units_of_cargo="TTD_STR_LITERS",
    items_of_cargo="string(STR_CARGO_UNIT_JET_FUEL)",
    penalty_lowerbound="18",
    single_penalty_length="255",
    capacity_multiplier="1",
    price_factor=150,
    icon_indices=(2, 4),  # FIRS PNW: borrowed slot of an unregistered FIRS cargo
    sprites_complete=True,
)
