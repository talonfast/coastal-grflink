from industry import IndustryPrimaryFuelled, IndustryPrimaryNoSupplies, IndustryPrimaryOrganic, IndustrySecondary, IndustryTertiary, TileLocationChecks

industry = IndustryTertiary(
    id="edeka_grocery_store",
    accept_cargo_types=["EGSW"],
    prob_in_game="3",
    prob_map_gen="6",
    prod_cargo_types=[],
    prod_multiplier="[0, 0]",
    map_colour="168",
    colour_scheme_name="scheme_3_hendrix",
    life_type="IND_LIFE_TYPE_BLACK_HOLE",
    prospect_chance="0.75",
    nearby_station_name="string(STR_STATION_TOWN_3)",
    fund_cost_multiplier="15",
    provides_snow=True,
    sprites_complete=True,
    animated_tiles_fixed=True,
    name="string(STR_IND_EDEKA_GROCERY_STORE)",
    special_flags=["IND_FLAG_ONLY_IN_TOWNS"],
    location_checks=dict(same_type_distance=16),
)

industry.enable_in_economy(
    "PACIFIC_NORTHWEST",
)




# industry.economy_variations['IN_A_HOT_COUNTRY'].accept_cargo_types = ['FOOD', 'GOOD', 'BEER', 'TEXT']



industry.add_tile(
    id="edeka_grocery_store_tile_1",
    location_checks=TileLocationChecks(require_road_adjacent=True),
)

spriteset_ground = industry.add_spriteset(
    type="pavement",
)
spriteset_ground_overlay = industry.add_spriteset(
    sprites=[(10, 10, 64, 31, -31, 0)],
)
spriteset_1 = industry.add_spriteset(sprites=[(10, 60, 64, 48, -31, -18)])
industry.add_spritelayout(
    id="edeka_grocery_store_spritelayout",
    tile="edeka_grocery_store_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[spriteset_1],
)
industry.add_industry_layout(
    id="edeka_grocery_store_industry_layout",
    layout=[(0, 0, "edeka_grocery_store_spritelayout")],
)
