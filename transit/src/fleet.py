"""The transit fleet: road vehicles (buses, streetcars, Link LRVs) and trains.

Order within each feature = engine ID, after OpenTTD's default vehicles so none is replaced:
road vehicles from 0x58, trains from 0x74. Append only!

Each entry is one engine. Buyable engines have a name; hidden ones (no name) are articulated parts
of the engine before them. `parts` lists the articulated parts after the front as (id, mirrored);
a mirrored part is drawn reversed (the rear cab). `gfx` names the model in vehicles.py (a mirrored
cab reuses the front cab's). `length` is in 1/8 of a standard vehicle. Weights are per part in
tonnes, capacities per part, speeds in km/h, power in hp. Figures are approximate real ones.
"""
import vehicles as V

RV_BASE, TRAIN_BASE = 0x58, 0x74

ROAD = [
    dict(id="enviro500", gfx="enviro500_classic", model=V.enviro500_classic, year=2008,
         name="BC Transit Enviro500 double-decker", kmh=80, hp=280, t=19, cap=90, cost=150, run=120,
         life=18, model_life=30,
         desc="Alexander Dennis tri-axle double-decker of the Victoria Regional Transit System, "
              "in the red, white and blue BC Transit livery."),
    dict(id="enviro500_green", gfx="enviro500_green", model=V.enviro500_green, year=2024,
         name="BC Transit Enviro500 double-decker (2024 livery)", variant_of="enviro500", kmh=80, hp=280,
         t=19, cap=90, cost=150, run=120, life=18, model_life=30,
         desc="The same bus in BC Transit's new green livery, on new buses from fall 2024."),
    dict(id="xde60", gfx="xde60_front", model=V.xde60_front, year=2018, parts=[("xde60_rear", False)],
         name="TransLink New Flyer XDE60 articulated bus", kmh=80, hp=280, t=12, cap=55, cost=160, run=130,
         life=16, model_life=30,
         desc="18 m diesel-electric hybrid articulated bus of Coast Mountain Bus Company, Metro Vancouver."),
    dict(id="xde60_rear", gfx="xde60_rear", model=V.xde60_rear, length=7, t=8, cap=45),
    dict(id="seattle", gfx="seattle_cab", model=V.seattle_cab, year=2007, tram=True,
         parts=[("seattle_mid", False), ("seattle_rear", True)],
         name="Seattle Streetcar Inekon 12 Trio", kmh=70, hp=480, t=11, cap=55, cost=170, run=140,
         life=30, model_life=40,
         desc="Three-section low-floor streetcar from Ostrava, built for the South Lake Union line."),
    dict(id="seattle_mid", gfx="seattle_mid", model=V.seattle_mid, length=4, tram=True, t=7, cap=30),
    dict(id="seattle_rear", gfx="seattle_cab", tram=True, t=11, cap=55),
    dict(id="portland", gfx="portland_cab", model=V.portland_cab, year=2001, tram=True,
         parts=[("portland_mid", False), ("portland_rear", True)],
         name="Portland Streetcar Skoda 10 T", kmh=70, hp=480, t=11, cap=60, cost=165, run=140,
         life=30, model_life=40,
         desc="The Czech-built low-floor car that opened North America's first modern streetcar line."),
    dict(id="portland_mid", gfx="portland_mid", model=V.portland_mid, length=4, tram=True, t=7, cap=37),
    dict(id="portland_rear", gfx="portland_cab", tram=True, t=11, cap=60),
    dict(id="link1", gfx="link1_cab", model=V.link1_cab, year=2009, tram=True,
         parts=[("link1_mid", False), ("link1_rear", True)],
         name="Sound Transit Link Kinkisharyo LRV", kmh=90, hp=790, t=19, cap=80, cost=200, run=150,
         life=30, model_life=35,
         desc="Series 1 light rail vehicle of Seattle's Link, here running as a tram."),
    dict(id="link1_mid", gfx="link1_mid", model=V.link1_mid, length=6, tram=True, t=10, cap=40),
    dict(id="link1_rear", gfx="link1_cab", tram=True, t=19, cap=80),
    dict(id="link2", gfx="link2_cab", model=V.link2_cab, year=2021, tram=True, variant_of="link1",
         parts=[("link2_mid", False), ("link2_rear", True)],
         name="Sound Transit Link Siemens S70 LRV", kmh=90, hp=790, t=19, cap=80, cost=205, run=150,
         life=30, model_life=35,
         desc="Series 2 light rail vehicle with bigger windows and more room for bikes, here running as a tram."),
    dict(id="link2_mid", gfx="link2_mid", model=V.link2_mid, length=6, tram=True, t=10, cap=40),
    dict(id="link2_rear", gfx="link2_cab", tram=True, t=19, cap=80),
    dict(id="edeka_truck", gfx="edeka_truck", model=V.edeka_truck, year=1970, cargo=["EGSW"],
         name="EDEKA delivery truck", kmh=90, hp=250, t=8, cap=20, cost=90, run=90, life=15, model_life=40,
         desc="Box truck in EDEKA yellow and blue for FIRS PNW's EDEKA Gouda Sandwiches. Carries nothing else."),
]

RAIL = [
    dict(id="mk5", gfx="mk5_cab", model=V.mk5_cab, year=2025, traction="electric", mu=True,
         parts=[("mk5_mid", False), ("mk5_mid", False), ("mk5_mid", False), ("mk5_rear", True)],
         name="TransLink SkyTrain Mark V", kmh=90, hp=1600, t=20, cap=150, cost=230, run=160,
         life=35, model_life=40,
         desc="Alstom's five-car SkyTrain for the Expo and Millennium lines, here running on electrified rail."),
    dict(id="mk5_mid", gfx="mk5_mid", model=V.mk5_mid, traction="electric", t=20, cap=160),
    dict(id="mk5_rear", gfx="mk5_cab", traction="electric", t=20, cap=150),
    dict(id="alc42e", gfx="alc42e", model=V.alc42e, year=2026, traction="diesel",
         name="Amtrak Cascades Airo ALC-42E", kmh=200, hp=4200, t=120, cap=0, cost=230, run=170,
         life=30, model_life=40,
         desc="Siemens Charger locomotive of the Airo trainsets, in service on the Cascades from 30 "
              "September 2026. Add Airo coaches and end the train with an Airo cab car."),
    dict(id="airo_coach", gfx="airo_coach", model=V.airo_coach, year=2026, wagon=True,
         name="Amtrak Cascades Airo coach", kmh=200, t=45, cap=66, cost=60, life=30, model_life=40,
         desc="Siemens Venture coach in the evergreen, cream and mocha Cascades livery."),
    dict(id="airo_cab", gfx="airo_cab", model=V.airo_cab, year=2026, wagon=True,
         name="Amtrak Cascades Airo cab car", kmh=200, t=48, cap=50, cost=70, life=30, model_life=40,
         desc="Coach with a driving cab at its back end: put it last in the train."),
    dict(id="aircraft_car", gfx="aircraft_car", model=V.aircraft_car, year=1968, wagon=True,
         cargo=["ACFT", "ACFC", "FLPL"], name="Aircraft flatcar", kmh=110, t=30, cap=1, cost=70, life=40,
         model_life=60,
         desc="Heavy flatcar for FIRS PNW's aircraft, certified aircraft and floatplanes, like the cars that bring "
              "Boeing's 737 fuselages to Renton."),
    dict(id="edeka_container_wagon", gfx="edeka_container_wagon", model=V.edeka_container_wagon, year=1970,
         wagon=True, cargo=["EGSW"], name="EDEKA container flatcar", kmh=120, t=22, cap=40, cost=60, life=35,
         model_life=50, desc="Two EDEKA reefer containers for FIRS PNW's EDEKA Gouda Sandwiches."),
]


def models():
    """{gfx name: model function} for every model to render."""
    return {e["gfx"]: e["model"] for e in ROAD + RAIL if "model" in e}
