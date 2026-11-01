from industry import IndustryPrimaryFuelled, IndustryPrimaryNoSupplies, IndustryPrimaryOrganic, IndustrySecondary, IndustryTertiary, TileLocationChecks

industry = IndustrySecondary(
    id="product_of_origin_sandwich_factory",
    accept_cargos_with_input_ratios=[("PODY", 8)],
    prod_cargo_types_with_output_ratios=[("EGSW", 8)],
    prob_in_game="3",
    prob_map_gen="5",
    map_colour="181",
    colour_scheme_name="scheme_1_elton",
    nearby_station_name="string(STR_STATION_FOOD_CORPORATION)",
    fund_cost_multiplier="65",
    sprites_complete=True,
    animated_tiles_fixed=True,
    name="string(STR_IND_PRODUCT_OF_ORIGIN_SANDWICH_FACTORY)",
)

industry.enable_in_economy(
    "PACIFIC_NORTHWEST",
)




industry.add_tile(
    id="product_of_origin_sandwich_factory_tile_1",
    location_checks=TileLocationChecks(
        require_effectively_flat=True, disallow_industry_adjacent=True
    ),
)

spriteset_ground = industry.add_spriteset(type="asphalt")
spriteset_ground_overlay = industry.add_spriteset(type="empty")
spriteset_1 = industry.add_spriteset(
    sprites=[(10, 10, 64, 87, -31, -56)],
)
spriteset_2 = industry.add_spriteset(
    sprites=[(80, 10, 64, 87, -31, -56)],
)
spriteset_3 = industry.add_spriteset(
    sprites=[(150, 10, 64, 87, -31, -56)],
)
spriteset_4 = industry.add_spriteset(
    sprites=[(220, 10, 64, 87, -31, -56)],
)

industry.add_spritelayout(
    id="product_of_origin_sandwich_factory_spritelayout_1",
    tile="product_of_origin_sandwich_factory_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[spriteset_1],
    add_to_object_num=1,
)
industry.add_spritelayout(
    id="product_of_origin_sandwich_factory_spritelayout_2",
    tile="product_of_origin_sandwich_factory_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[spriteset_2],
    fences=["nw", "ne", "se", "sw"],
    add_to_object_num=2,
)
industry.add_spritelayout(
    id="product_of_origin_sandwich_factory_spritelayout_3",
    tile="product_of_origin_sandwich_factory_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[spriteset_3],
    fences=["nw", "ne", "se", "sw"],
    add_to_object_num=3,
)
industry.add_spritelayout(
    id="product_of_origin_sandwich_factory_spritelayout_4",
    tile="product_of_origin_sandwich_factory_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[spriteset_4],
    fences=["nw", "ne", "se", "sw"],
    add_to_object_num=4,
)
industry.add_spritelayout(
    id="product_of_origin_sandwich_factory_spritelayout_empty",
    tile="product_of_origin_sandwich_factory_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[],
    fences=["nw", "ne", "se", "sw"],
    add_to_object_num=5,
)

industry.add_industry_layout(
    id="product_of_origin_sandwich_factory_industry_layout_1",
    layout=[
        (0, 0, "product_of_origin_sandwich_factory_spritelayout_1"),
        (0, 1, "product_of_origin_sandwich_factory_spritelayout_1"),
        (0, 2, "product_of_origin_sandwich_factory_spritelayout_3"),
        (1, 0, "product_of_origin_sandwich_factory_spritelayout_1"),
        (1, 1, "product_of_origin_sandwich_factory_spritelayout_1"),
        (1, 2, "product_of_origin_sandwich_factory_spritelayout_3"),
        (2, 0, "product_of_origin_sandwich_factory_spritelayout_2"),
        (2, 1, "product_of_origin_sandwich_factory_spritelayout_2"),
        (2, 2, "product_of_origin_sandwich_factory_spritelayout_4"),
        (3, 0, "product_of_origin_sandwich_factory_spritelayout_4"),
        (3, 1, "product_of_origin_sandwich_factory_spritelayout_4"),
        (3, 2, "product_of_origin_sandwich_factory_spritelayout_4"),
    ],
)
industry.add_industry_layout(
    id="product_of_origin_sandwich_factory_industry_layout_2",
    layout=[
        (0, 0, "product_of_origin_sandwich_factory_spritelayout_2"),
        (0, 1, "product_of_origin_sandwich_factory_spritelayout_3"),
        (0, 2, "product_of_origin_sandwich_factory_spritelayout_1"),
        (0, 3, "product_of_origin_sandwich_factory_spritelayout_3"),
        (1, 0, "product_of_origin_sandwich_factory_spritelayout_1"),
        (1, 1, "product_of_origin_sandwich_factory_spritelayout_4"),
        (1, 2, "product_of_origin_sandwich_factory_spritelayout_1"),
        (1, 3, "product_of_origin_sandwich_factory_spritelayout_3"),
        (2, 0, "product_of_origin_sandwich_factory_spritelayout_2"),
        (2, 1, "product_of_origin_sandwich_factory_spritelayout_4"),
        (2, 2, "product_of_origin_sandwich_factory_spritelayout_1"),
        (3, 0, "product_of_origin_sandwich_factory_spritelayout_2"),
        (3, 1, "product_of_origin_sandwich_factory_spritelayout_4"),
        (3, 2, "product_of_origin_sandwich_factory_spritelayout_1"),
    ],
)
industry.add_industry_layout(
    id="product_of_origin_sandwich_factory_industry_layout_3",
    layout=[
        (0, 0, "product_of_origin_sandwich_factory_spritelayout_1"),
        (0, 1, "product_of_origin_sandwich_factory_spritelayout_1"),
        (0, 2, "product_of_origin_sandwich_factory_spritelayout_2"),
        (0, 3, "product_of_origin_sandwich_factory_spritelayout_3"),
        (1, 0, "product_of_origin_sandwich_factory_spritelayout_1"),
        (1, 1, "product_of_origin_sandwich_factory_spritelayout_1"),
        (1, 2, "product_of_origin_sandwich_factory_spritelayout_2"),
        (1, 3, "product_of_origin_sandwich_factory_spritelayout_3"),
        (2, 0, "product_of_origin_sandwich_factory_spritelayout_1"),
        (2, 1, "product_of_origin_sandwich_factory_spritelayout_1"),
        (2, 2, "product_of_origin_sandwich_factory_spritelayout_4"),
        (2, 3, "product_of_origin_sandwich_factory_spritelayout_4"),
    ],
)
