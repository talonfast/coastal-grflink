from industry import IndustryPrimaryFuelled, IndustryPrimaryNoSupplies, IndustryPrimaryOrganic, IndustrySecondary, IndustryTertiary, TileLocationChecks

industry = IndustryPrimaryNoSupplies(
    id="oil_terminal",
    scenario_only=True,
    accept_cargo_types=[],
    prod_cargo_types_with_multipliers=[("OIL_", 28)],
    prob_in_game="0",
    prob_map_gen="0",
    map_colour="151",
    colour_scheme_name="scheme_3_hendrix",
    prospect_chance="0.75",
    fund_cost_multiplier="230",
    nearby_station_name="string(STR_STATION_WELLS)",
    provides_snow=True,
    primary_production_random_factor_set="medium_range",
    sprites_complete=True,
    animated_tiles_fixed=True,
    name="string(STR_IND_OIL_TERMINAL)",
)

industry.enable_in_economy(
    "PACIFIC_NORTHWEST",
)



industry.add_tile(
    id="oil_terminal_tile_1",
    location_checks=TileLocationChecks(disallow_industry_adjacent=True),
)

spriteset_ground = industry.add_spriteset(
    type="asphalt",
)
spriteset_ground_overlay = industry.add_spriteset(
    type="empty",
)

industry.add_spritelayout(
    id="oil_terminal_spritelayout_0_0",
    tile="oil_terminal_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(10, 10, 67, 37, -33, -3)])],
    fences=[],
)

industry.add_spritelayout(
    id="oil_terminal_spritelayout_0_1",
    tile="oil_terminal_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(87, 10, 67, 38, -33, -4)])],
    fences=[],
)

industry.add_spritelayout(
    id="oil_terminal_spritelayout_1_0",
    tile="oil_terminal_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(164, 10, 67, 38, -33, -4)])],
    fences=[],
)

industry.add_spritelayout(
    id="oil_terminal_spritelayout_1_1",
    tile="oil_terminal_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(241, 10, 67, 39, -33, -5)])],
    fences=[],
)

industry.add_spritelayout(
    id="oil_terminal_spritelayout_2_0",
    tile="oil_terminal_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(318, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_spritelayout(
    id="oil_terminal_spritelayout_2_1",
    tile="oil_terminal_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(395, 10, 67, 37, -33, -3)])],
    fences=[],
)

industry.add_industry_layout(
    id="oil_terminal_industry_layout_1",
    layout=[
        (0, 0, "oil_terminal_spritelayout_0_0"),
        (0, 1, "oil_terminal_spritelayout_0_1"),
        (1, 0, "oil_terminal_spritelayout_1_0"),
        (1, 1, "oil_terminal_spritelayout_1_1"),
        (2, 0, "oil_terminal_spritelayout_2_0"),
        (2, 1, "oil_terminal_spritelayout_2_1"),
    ],
)
