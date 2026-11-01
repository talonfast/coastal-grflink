from industry import IndustryPrimaryFuelled, IndustryPrimaryNoSupplies, IndustryPrimaryOrganic, IndustrySecondary, IndustryTertiary, TileLocationChecks

industry = IndustrySecondary(
    id="floatplane_factory",
    scenario_only=True,
    accept_cargos_with_input_ratios=[("ALUM", 4), ("ACPT", 4)],
    prod_cargo_types_with_output_ratios=[("FLPL", 8)],
    prob_in_game="0",
    prob_map_gen="0",
    map_colour="194",
    colour_scheme_name="scheme_1_elton",
    nearby_station_name="string(STR_STATION_APPLIANCE_FACTORY)",
    fund_cost_multiplier="120",
    pollution_and_squalor_factor=1,
    sprites_complete=True,
    animated_tiles_fixed=True,
    name="string(STR_IND_FLOATPLANE_FACTORY)",
)

industry.enable_in_economy(
    "PACIFIC_NORTHWEST",
)


industry.add_tile(
    id="floatplane_factory_tile_1",
    location_checks=TileLocationChecks(disallow_industry_adjacent=True),
)

spriteset_ground = industry.add_spriteset(
    type="asphalt",
)
spriteset_ground_overlay = industry.add_spriteset(
    type="empty",
)

industry.add_spritelayout(
    id="floatplane_factory_spritelayout_0_0",
    tile="floatplane_factory_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(10, 10, 67, 50, -33, -16)])],
    fences=[],
)

industry.add_spritelayout(
    id="floatplane_factory_spritelayout_0_1",
    tile="floatplane_factory_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(87, 10, 67, 53, -33, -19)])],
    fences=[],
)

industry.add_spritelayout(
    id="floatplane_factory_spritelayout_1_0",
    tile="floatplane_factory_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(164, 10, 67, 51, -33, -17)])],
    fences=[],
)

industry.add_spritelayout(
    id="floatplane_factory_spritelayout_1_1",
    tile="floatplane_factory_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(241, 10, 67, 55, -33, -21)])],
    fences=[],
)

industry.add_industry_layout(
    id="floatplane_factory_industry_layout_1",
    layout=[
        (0, 0, "floatplane_factory_spritelayout_0_0"),
        (0, 1, "floatplane_factory_spritelayout_0_1"),
        (1, 0, "floatplane_factory_spritelayout_1_0"),
        (1, 1, "floatplane_factory_spritelayout_1_1"),
    ],
)
