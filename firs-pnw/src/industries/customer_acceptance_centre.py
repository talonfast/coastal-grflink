from industry import IndustryPrimaryFuelled, IndustryPrimaryNoSupplies, IndustryPrimaryOrganic, IndustrySecondary, IndustryTertiary, TileLocationChecks

industry = IndustryTertiary(
    id="customer_acceptance_centre",
    scenario_only=True,
    accept_cargo_types=["ACFT", "ACFC"],
    prod_cargo_types_with_multipliers=[],
    prob_in_game="0",
    prob_map_gen="0",
    map_colour="207",
    colour_scheme_name="scheme_1_elton",
    life_type="IND_LIFE_TYPE_BLACK_HOLE",
    prospect_chance="0.75",
    nearby_station_name="string(STR_STATION_VEHICLE_DISTRIBUTOR)",
    fund_cost_multiplier="8",
    provides_snow=True,
    sprites_complete=True,
    animated_tiles_fixed=True,
    name="string(STR_IND_CUSTOMER_ACCEPTANCE_CENTRE)",
)

industry.enable_in_economy(
    "PACIFIC_NORTHWEST",
)


industry.add_tile(
    id="customer_acceptance_centre_tile_1",
    location_checks=TileLocationChecks(disallow_industry_adjacent=True),
)

spriteset_ground = industry.add_spriteset(
    type="asphalt",
)
spriteset_ground_overlay = industry.add_spriteset(
    type="empty",
)

industry.add_spritelayout(
    id="customer_acceptance_centre_spritelayout_0_0",
    tile="customer_acceptance_centre_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(10, 10, 67, 48, -33, -14)])],
    fences=[],
)

industry.add_spritelayout(
    id="customer_acceptance_centre_spritelayout_0_1",
    tile="customer_acceptance_centre_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(87, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_spritelayout(
    id="customer_acceptance_centre_spritelayout_1_0",
    tile="customer_acceptance_centre_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(164, 10, 67, 50, -33, -16)])],
    fences=[],
)

industry.add_spritelayout(
    id="customer_acceptance_centre_spritelayout_1_1",
    tile="customer_acceptance_centre_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[(241, 10, 67, 36, -33, -2)])],
    fences=[],
)

industry.add_industry_layout(
    id="customer_acceptance_centre_industry_layout_1",
    layout=[
        (0, 0, "customer_acceptance_centre_spritelayout_0_0"),
        (0, 1, "customer_acceptance_centre_spritelayout_0_1"),
        (1, 0, "customer_acceptance_centre_spritelayout_1_0"),
        (1, 1, "customer_acceptance_centre_spritelayout_1_1"),
    ],
)
