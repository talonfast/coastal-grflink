from cargo import Cargo

cargo = Cargo(
    id="product_of_origin_dairy",
    type_name="string(STR_CARGO_NAME_PRODUCT_OF_ORIGIN_DAIRY)",
    unit_name="string(STR_CARGO_NAME_PRODUCT_OF_ORIGIN_DAIRY)",
    type_abbreviation="string(STR_CID_PRODUCT_OF_ORIGIN_DAIRY)",
    sprite="NEW_CARGO_SPRITE",
    weight="1.1",
    is_freight="1",
    cargo_classes = ['CC_EXPRESS', 'CC_LIQUID_BULK', 'CC_POTABLE', 'CC_REFRIGERATED'],
    cargo_label="PODY",
    units_of_cargo="TTD_STR_LITERS",
    items_of_cargo="string(STR_CARGO_UNIT_PRODUCT_OF_ORIGIN_DAIRY)",
    penalty_lowerbound="0",
    single_penalty_length="16",
    capacity_multiplier="1",
    price_factor=140,
    icon_indices=(0, 3),  # FIRS PNW: borrowed slot of an unregistered FIRS cargo
    sprites_complete=True,
)
