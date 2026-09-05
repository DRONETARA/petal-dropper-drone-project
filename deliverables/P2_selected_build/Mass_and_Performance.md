# P2 mass and performance sizing

The planning total is **20.28 kg**, including **1.000 kg of petals** and 0.500 kg of contingency. The design ceiling is 21 kg, leaving another 0.72 kg before that ceiling. This is not weighed mass or an approved takeoff limit. See `Mass_budget.csv` and `sizing.json` for reproducible inputs.

| Item | kg | Basis |
|---|---:|---|
| Printed attachment | 3.751 | CAD solid volume; assumed PETG 1.27 g/cm3 |
| Attachment rails/fasteners/cords/cover/horns | 1.000 | Planning allowance, excludes servos |
| Two release servos | 0.132 | Published, excluding horns |
| Four propulsion units | 2.992 | Published with props and cables |
| Battery | 4.650 | Published nominal; custom-tail difference in harness allowance |
| Carbon centre plates | 1.525 | CAD volume; assumed CFRP 1.6 g/cm3 |
| Machined arm clamps | 0.922 | CAD volume; assumed aluminium 2.7 g/cm3 |
| Carbon arms | 0.441 | Supplier linear mass x nominal tube length |
| Tubular landing members | 1.414 | CAD volume; assumed aluminium 2.7 g/cm3 |
| Landing saddles/gussets/pads | 0.200 | Allowance beyond tubular members |
| Aircraft fasteners | 0.550 | Allowance including washers, nuts and mounting bolts |
| FC/PM/GPS/RX/BEC | 0.370 | Published component masses, approximate |
| Power distribution, fuse, connector, added wiring | 0.650 | Allowance; weigh custom harness |
| Straps/foam/avionics supports | 0.180 | Allowance |
| Petals | 1.000 | Required payload alone |
| Unallocated mass contingency | 0.500 | Planning reserve |

Thin printed walls remain largely solid regardless of infill. Do not subtract a guessed infill percentage from the whole attachment. Actual fasteners, battery termination, weld gussets, supports and wire routing may exceed their allowances. Weigh the complete aircraft after assembly; if it exceeds 21 kg, reduce mass or resize/requalify the propulsion.

## Lift and current

At 21 kg, hover requires 5.25 kg thrust per motor. Interpolation between the manufacturer's 46 V laboratory points (4,712 g at 12.4 A and 5,256 g at 14.7 A) gives approximately **58.7 A total / 2.70 kW**. This is a static sea-level estimate at the cited test conditions, not a flight measurement. The manufacturer's recommended 4–6 kg-per-axis range supports choosing this motor family. [Hobbywing X6 Plus G2](https://www.hobbywing.com/en/products/x6-plus-g2)

The published maximum 12.526 kg per unit would total 50.104 kg and a 2.39:1 ratio at 21 kg, but that maximum is outside the proposed routine electrical envelope and cannot be treated as continuous thrust. The integrated ESC's 25 A continuous rating limits four-unit continuous current to 100 A before accessory allowance; individual motor currents must also remain within their ratings. PM08's 200 A rating is not the motor limit.

For initial qualification, target at most **160 A bus for a maximum two-second transient**, below 100 A total propulsion current continuously, and verify each ESC separately. A preliminary command ceiling near the 78% laboratory point corresponds to 156.8 A and 39.144 kg total static thrust at 46 V, or 1.86:1 at 21 kg. Percent bench throttle is not guaranteed to map exactly to an autopilot parameter. Establish the actual PWM ceiling with current/thrust measurements at a full 50.4 V battery before flight. Servo/accessory current also belongs in the bus total.

A hypothetical 20% thrust derating reduces that transient figure to 31.315 kg, only 1.49:1 at 21 kg. To retain a 1.8:1 transient ratio in that scenario, mass would need to be at most 17.40 kg. Therefore this selection does **not** establish hot/high-altitude performance; qualify the intended environment or revise mass/propulsion. Software current limiting reacts too slowly to substitute for electrical sizing.

## Endurance and geometry

The standard 12S 22 Ah pack is nominally 976.8 Wh. Reserving 25% energy and adding 15% to the bench hover power plus 20 W for electronics gives approximately **14.1 minutes of analytical hover** at the 21 kg ceiling. Wind, manoeuvres, voltage sag, temperature, battery ageing and reserve policy change this. It is not a promised flight duration. [Battery specification](https://www.grepow.com/uav-battery/tattu-12s-lipo-drone-battery.html)

Adjacent motor centres are 919.24 mm apart. A nominal 620 mm swept diameter leaves 299.24 mm between adjacent rotor disks in plan. The detailed pod outline is approximate; confirm actual insertion and final rotor centres. Battery and GPS envelopes lie inside the central clear region. The mechanism's sampled minimum door-ground gap is recorded independently in `final_checks.json`; do not confuse it with clearance under pitch/roll or uneven ground.

The centered battery and hopper support a roughly centered plan CG, but hardware distribution and departing petals change it. Measure full/empty CG and recheck stability; no inertia model or autopilot tuning was completed.

## Release actuator and structure

The selected D954SW at 7.4 V has published 29 kgf·cm stall torque (2.844 N·m), 5.8 kgf·cm peak-efficiency torque (0.569 N·m), and 5.2 A stall current. Neither torque number is a continuous application rating. [Hitec drawing/data](https://www.hiteccs.com/public/uploads/data_sheet/HRC_D954SW_Specsheetv2.2_102-1729877827.pdf)

An intentionally conservative friction estimate of 0.4 × (1.7 kg ×9.81) ×0.060 m is 0.400 N·m if one keeper briefly carries that whole load. Real hinge load sharing may lower it; petal snagging may raise it. A threefold design target would require 1.20 N·m of verified short-duration output at the actual voltage/duty, not merely a larger stall number. This has not been demonstrated. Measure breakaway torque and actual loaded release current/temperature; change the actuator or bearing/contact design if margin is insufficient.

For a provisional 3g sizing case, a 21 kg aircraft corresponds to 618 N overall. An attachment around 6 kg corresponds to 177 N, nominally 44 N per suspension point under ideal sharing. Unequal load distribution, landing shocks, creep and layer adhesion invalidate treating those as certified loads. The frame/printed mounts still require engineering proof loads based on actual material properties and intended use. CAD topology and absence of sampled collision do not establish strength.
