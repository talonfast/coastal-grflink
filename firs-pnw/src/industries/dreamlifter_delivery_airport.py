from industry import IndustryPrimaryFuelled, IndustryPrimaryNoSupplies, IndustryPrimaryOrganic, IndustrySecondary, IndustryTertiary, TileLocationChecks

industry = IndustryPrimaryFuelled(
    id="dreamlifter_delivery_airport",
    scenario_only=True,
    accept_cargo_types=["JETF"],
    prod_cargo_types_with_multipliers=[("ACPT", 20)],
    prob_in_game="0",
    prob_map_gen="0",
    map_colour="209",
    colour_scheme_name="scheme_3_hendrix",
    prospect_chance="0.75",
    fund_cost_multiplier="230",
    nearby_station_name="string(STR_STATION_WELLS)",
    provides_snow=True,
    primary_production_random_factor_set="medium_range",
    sprites_complete=True,
    animated_tiles_fixed=True,
    name="string(STR_IND_DREAMLIFTER_DELIVERY_AIRPORT)",
)

industry.enable_in_economy(
    "PACIFIC_NORTHWEST",
)



industry.add_tile(
    id="dreamlifter_delivery_airport_tile_1",
    location_checks=TileLocationChecks(disallow_industry_adjacent=True),
)

spriteset_ground = industry.add_spriteset(
    type="asphalt",
)
spriteset_ground_overlay = industry.add_spriteset(
    type="empty",
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_0_0",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(10, 10, 67, 44, -33, -10)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_0_1",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(87, 10, 67, 49, -33, -15)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_0_2",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(164, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_1_0",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(241, 10, 67, 48, -33, -14)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_1_1",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(318, 10, 67, 53, -33, -19)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_1_2",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(395, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_2_0",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(472, 10, 67, 56, -33, -22)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_2_1",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(549, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_2_2",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(626, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_3_0",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(703, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_3_1",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(780, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_3_2",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(857, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_4_0",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(934, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_4_1",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(1011, 10, 81, 64, -33, -30)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_4_2",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(1102, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_5_0",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(1179, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_5_1",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(1256, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_spritelayout(
    id="dreamlifter_delivery_airport_spritelayout_5_2",
    tile="dreamlifter_delivery_airport_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(1333, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_industry_layout(
    id="dreamlifter_delivery_airport_industry_layout_1",
    layout=[
        (0, 0, "dreamlifter_delivery_airport_spritelayout_0_0"),
        (0, 1, "dreamlifter_delivery_airport_spritelayout_0_1"),
        (0, 2, "dreamlifter_delivery_airport_spritelayout_0_2"),
        (1, 0, "dreamlifter_delivery_airport_spritelayout_1_0"),
        (1, 1, "dreamlifter_delivery_airport_spritelayout_1_1"),
        (1, 2, "dreamlifter_delivery_airport_spritelayout_1_2"),
        (2, 0, "dreamlifter_delivery_airport_spritelayout_2_0"),
        (2, 1, "dreamlifter_delivery_airport_spritelayout_2_1"),
        (2, 2, "dreamlifter_delivery_airport_spritelayout_2_2"),
        (3, 0, "dreamlifter_delivery_airport_spritelayout_3_0"),
        (3, 1, "dreamlifter_delivery_airport_spritelayout_3_1"),
        (3, 2, "dreamlifter_delivery_airport_spritelayout_3_2"),
        (4, 0, "dreamlifter_delivery_airport_spritelayout_4_0"),
        (4, 1, "dreamlifter_delivery_airport_spritelayout_4_1"),
        (4, 2, "dreamlifter_delivery_airport_spritelayout_4_2"),
        (5, 0, "dreamlifter_delivery_airport_spritelayout_5_0"),
        (5, 1, "dreamlifter_delivery_airport_spritelayout_5_1"),
        (5, 2, "dreamlifter_delivery_airport_spritelayout_5_2"),
    ],
)
