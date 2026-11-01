from industry import IndustryPrimaryFuelled, IndustryPrimaryNoSupplies, IndustryPrimaryOrganic, IndustrySecondary, IndustryTertiary, TileLocationChecks

industry = IndustrySecondary(
    id="aircraft_assembly_plant",
    scenario_only=True,
    accept_cargos_with_input_ratios=[("ALUM", 4), ("ACPT", 4)],
    prod_cargo_types_with_output_ratios=[("ACFT", 8)],
    prob_in_game="0",
    prob_map_gen="0",
    map_colour="141",
    colour_scheme_name="scheme_7_bowie",
    nearby_station_name="string(STR_STATION_AUTOMOTIVE)",
    fund_cost_multiplier="145",
    sprites_complete=True,
    animated_tiles_fixed=True,
    name="string(STR_IND_AIRCRAFT_ASSEMBLY_PLANT)",
)

industry.enable_in_economy(
    "PACIFIC_NORTHWEST",
)


industry.add_tile(
    id="aircraft_assembly_plant_tile_1",
    location_checks=TileLocationChecks(disallow_industry_adjacent=True),
)

spriteset_ground = industry.add_spriteset(
    type="asphalt",
)
spriteset_ground_overlay = industry.add_spriteset(
    type="empty",
)

industry.add_spritelayout(
    id="aircraft_assembly_plant_spritelayout_0_0",
    tile="aircraft_assembly_plant_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(10, 10, 67, 59, -33, -25)])],
    fences=[],
)

industry.add_spritelayout(
    id="aircraft_assembly_plant_spritelayout_0_1",
    tile="aircraft_assembly_plant_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(87, 10, 67, 59, -33, -25)])],
    fences=[],
)

industry.add_spritelayout(
    id="aircraft_assembly_plant_spritelayout_1_0",
    tile="aircraft_assembly_plant_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(164, 10, 67, 60, -33, -26)])],
    fences=[],
)

industry.add_spritelayout(
    id="aircraft_assembly_plant_spritelayout_1_1",
    tile="aircraft_assembly_plant_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(241, 10, 67, 60, -33, -26)])],
    fences=[],
)

industry.add_spritelayout(
    id="aircraft_assembly_plant_spritelayout_2_0",
    tile="aircraft_assembly_plant_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(318, 10, 67, 60, -33, -26)])],
    fences=[],
)

industry.add_spritelayout(
    id="aircraft_assembly_plant_spritelayout_2_1",
    tile="aircraft_assembly_plant_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(395, 10, 67, 60, -33, -26)])],
    fences=[],
)

industry.add_industry_layout(
    id="aircraft_assembly_plant_industry_layout_1",
    layout=[
        (0, 0, "aircraft_assembly_plant_spritelayout_0_0"),
        (0, 1, "aircraft_assembly_plant_spritelayout_0_1"),
        (1, 0, "aircraft_assembly_plant_spritelayout_1_0"),
        (1, 1, "aircraft_assembly_plant_spritelayout_1_1"),
        (2, 0, "aircraft_assembly_plant_spritelayout_2_0"),
        (2, 1, "aircraft_assembly_plant_spritelayout_2_1"),
    ],
)
