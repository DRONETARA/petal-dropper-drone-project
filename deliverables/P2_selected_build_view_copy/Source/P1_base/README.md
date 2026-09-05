# PetalDrop P1 — 1 kg petal-target bench prototype

**The target is at least 1 kg of flower petals alone.** The previous 200 g request is superseded. This package contains an editable drone-and-attachment assembly, 46 separate printable attachment parts, and an illustrated release/reset sequence. It is an untested mechanical prototype, not a demonstrated 1 kg-capable aircraft or a physically validated release system.

The original `Dronetara_Starter.blend` and its preview remain unchanged in the parent output folder. The new assembly uses the original visual drone enlarged **2.5 times in physical dimensions**, with an illustrative extended landing stand. That enlargement does not establish motor thrust, frame strength, endurance, or payload rating.

## Files and operation

- `PetalDrop_1kg_Assembly.blend`: editable assembly. One Blender unit represents one millimetre (`scale_length = 0.001`). Printable components are grouped in collections 10–14; purchased hardware and reference parts are separate.
- `STL_mm/`: 46 individual attachment components, one copy of each filename. STL has no intrinsic unit field: import as **millimetres, at 100% scale**. These files do not contain the decorative drone or landing stand.
- `parts_manifest.csv` / `.json`: each part's dimensions, quantity, nominal solid PETG mass and notes.
- `Assembly_closed.png`, `Assembly_open.png`: complete aircraft/reference-attachment views.
- `Mechanism_open.png`: better-lit underside detail; reference landing legs are hidden for this image only.
- `verification.json`: Blender topology, nominal wall/volume data and timeline collision sampling.
- `final_checks.json`: independent validation of the delivered STL binaries and a one-degree mechanism sweep, including reference landing legs.
- `limit_cords.json`: provisional door-stop cord lengths and assumptions.
- `hardware_BOM.csv`: purchased/fabricated hardware, separate from the print list.

Timeline markers describe the mechanism, rather than a physics simulation:

| Frames | State |
|---|---|
| 1 | Doors closed; keepers overlap the door ribs; removable transport pins installed |
| 20 | Both transport pins removed; operator has armed the mechanism |
| 20–50 | Two servos rotate the mechanical keepers through 90 degrees |
| 50–90 | Both doors swing down under gravity to the provisional 95-degree cord limit |
| 90–105 | Discharge opening exposed |
| 105–125 | **Manual** lifting of the empty doors, represented by keyframes |
| 125–155 | Servos return the keepers under the raised doors |
| 180 | Transport pins reinstalled |

This design intentionally uses gravity opening and manual reset. The servos do not lift 1 kg of petals or raise the doors. Support both empty doors by hand during reset, then close the keepers and insert the transport pins. Never command keeper closure into partly raised doors.

## Geometry and capacity assumptions

| Item | Provisional value |
|---|---:|
| Internal hopper plan | 320 × 320 mm |
| Interior bottom datum / top | Z354 / Z590 mm |
| Nominal gross enclosed volume | 24.166 L |
| Fill line | Z570 mm; 20 mm below the top |
| Geometric volume below fill line | 22.118 L, before displacement by hardware/cover |
| Minimum bulk density for 1 kg in that volume | 45.21 kg/m³; actual required density is slightly higher with displaced volume |
| Clear throat between support lips | 292 × 292 mm |
| Main hopper walls / bolt flanges | 2.4 / 4 mm |
| Door skins / ribs below skins | 2.4 / 9.6 mm |
| Module seam gap | 0.4 mm, sealed externally after assembly |
| Closed door skin to throat lip | 2 mm nominal vertical gap |
| Closed keeper to door rib | 0.5 mm nominal gap; doors settle onto keepers under load |
| Hinge pin / printed bore | 5.0 / 5.4 mm |
| Door knuckle to clevis | 2 mm nominal axial clearance at each end |
| Common M4 clearance holes | 4.4 mm |
| Provisional printer envelope | 220 × 220 × 220 mm |

The smooth interior and broad bottom opening reduce small-throat bridging risk, but wet petals, tangled petals and propwash can still prevent clean release. The cover is a **nonprinted fabric/net retention cover**, not a printed lid. Secure it around the rim and reinforce its four suspension-stud openings. The cover and fasteners displace some of the geometric volume.

### Measure the petals before claiming capacity

1. Weigh representative petals using the same variety, moisture and handling expected in use.
2. Fill a known-volume container loosely, without compressing the petals to make them fit. Repeat several times, including the loosest expected batch.
3. Compute bulk density as `mass_kg / volume_m³`, or required volume as `1 kg / measured density`.
4. Then test a full 1 kg batch in the assembled hopper below the fill line, with the cover installed. Record residual petals after release.

If the loosest batch needs more than the usable volume, this hopper does **not** meet the 1 kg requirement for that batch. Increase hopper volume or change the loading method and recheck the mechanism, mass, printer splits and clearances. No petal density was invented or measured during this design task.

## Mechanical load path and restraint

Petals rest on the ribbed doors. Door load is shared by the four steel-pin hinges and two wide keeper dogs. Each keeper overlaps the inner edges of **both** doors. Its axial load passes through a thrust washer into the printed carrier shelf, then through M4 fasteners into the hopper. The servo supplies rotation through a separate 6 mm spindle; its output bearing is not the intended vertical load support.

Hopper forces pass through the bolted corner shells to four suspension brackets, four M6 studs and two aluminium square-tube rails. Four rail clamps show a provisional connection to the visual airframe. Use through-bolts, washers and locking nuts rather than relying on printed threads.

Four adjustable, **nonprinted** 2 mm limit cords connect the keeper-carrier shelves to eye bolts on the door end ribs. Their geometry provides a nominal 95-degree opening stop. See `limit_cords.json` for eye-centre length; add the actual eye/loop/knot allowance and adjust on the physical assembly. Cord shape in Blender is illustrative. Verify routing, abrasion, shock load, knot security and angle before operating. The eye bolts and cord anchors are not strength-certified.

The small torsion-spring shapes are explicitly **hardware placeholders**. A spring, its end anchors and preload have not been selected or engineered. Do not rely on these shapes for automatic return or a power-loss fail-safe. The removable 3 mm transport pins are positive mechanical restraints when installed; remove both before servo actuation. Determine the required in-service power-loss behaviour before any aircraft integration.

## Mass, lift and actuator requirements

The mesh-volume estimate is approximately **3.73 kg for fully solid PETG**, using an assumed density of 1.27 g/cm³. This is not a slicer result or weighed mass. Infill may reduce some thick-part mass, while supports, hardware and finishing change the actual totals. Thin walls cannot be treated as empty infill volumes.

| Load item | Current status |
|---|---|
| Petals | Required target: **at least 1.000 kg** |
| Printed attachment | Approximately 3.73 kg if solid PETG; see manifest for exact current estimate |
| Rails, studs, fasteners, actuators, cover, cords, wiring | Provisional planning allowance **1.0–1.4 kg**; choose and weigh actual hardware |
| Added load carried by aircraft | Approximately **5.7–6.1 kg** under the solid-print assumption, excluding any new landing gear |
| Actual drone empty mass, lift margin and endurance | Unknown |

The attachment is therefore a substantial bench prototype, not a demonstrated lightweight flight payload. Slicer estimates and a weighed build are required before matching it to an airframe. The visual drone's propellers, motors and enlarged geometry supply no evidence of lift capacity.

For an **illustrative, unvalidated 3 g load case**, 5.7–6.1 kg creates about 168–180 N total vertical force, or 42–45 N per suspension point if perfectly shared. Real loads need not share evenly. This calculation is a sizing input only: no material coupon testing, stress analysis, fatigue assessment, pull-out test or structural proof test was performed.

Each servo model is a placeholder, not a verified purchasable actuator. The current interface assumes:

- Body envelope: 40.5 × 20.5 × 40 mm, with shaft axis offset 10 mm from body centre.
- Ear-hole pattern: 49.5 × 10 mm, using 3.4 mm printed clearance holes.
- Purchased horn: four M2.5 attachment screws on a **provisional 17 mm pitch circle**.
- Separate 6 mm steel spindle with two M3 cross-bolt connections. Confirm actual shaft machining, fit, fastener strength and access.
- At least 90 degrees of usable commanded travel, with calibrated closed/open limits.

A conservative starting selection calculation is `T ≈ friction coefficient × supported force × contact radius`. Assuming 0.4 friction, about 1.7 kg of doors plus petals temporarily loading one keeper, and a 60 mm effective radius gives roughly **0.4 N·m**. A factor of three gives **1.2 N·m of verified usable torque**, before spring, dirt or jam allowances. This is not a stall-torque endorsement or a measured requirement. Select the actuator using its real voltage, duty and torque data, then rework the provisional horn adapter and carrier if needed.

Power the actuators from a correctly rated supply/BEC; establish stall/current demand and signal compatibility from the selected hardware. Do not assume an autopilot's signal header can power two high-torque servos. No autopilot wiring, software or failsafe configuration is supplied because the controller is unknown.

## Printing and assembly

All 46 files fit within the provisional 220 mm cube. Each STL is translated to the build plane and oriented along a bounding-box axis; this is a packaging orientation, **not a guarantee of support-free printing or optimal layer strength**. Confirm orientation in the slicer.

Suggested starting process: calibrated 0.4 mm nozzle and 0.2 mm layers. The 2.4 mm skins are nominally six 0.4 mm extrusion widths, but actual slicer line width matters. Print a hinge/clearance sample before the full set. Use a suitable tested material profile and orient structural brackets so primary loads do not simply peel apart layer interfaces. No generic infill percentage establishes strength.

1. Assemble the eight hopper corner modules with M4 screws, wide washers and locknuts. Keep the 0.4 mm seam gaps consistent and seal them externally. Do not rely on adhesive alone.
2. Add the eight throat rails, four hinge clevises and four upper suspension brackets using their matching through-holes.
3. Join each two-tile door using its two underside splice plates. Fit steel hinge pins, thrust washers and positive pin retention. Check free rotation with the servos/cords disconnected.
4. Assemble each keeper carrier, thrust washer, spindle, keeper and **hardware-matched** horn adapter. Install the selected actuator and verify its mounting and output axis before tightening.
5. Fit the four M4 limit-cord eye anchors on carriers and four on doors. Adjust the four cords evenly while physically supporting the open doors. Check that slack cords stay clear of latches, shafts and the release opening.
6. Fit the M6 suspension studs, rails and removable rail clamps. The airframe interface must be adapted to the actual frame, not drilled from the decorative model by assumption.
7. Secure the fabric cover, wiring and any tethering so nothing can enter the propellers or catch a door.

Fastener lengths in the BOM are provisional. Measure the assembled stack, allow full nut engagement, retain moving pins, and check that projecting threads do not obstruct petals or moving parts.

## Verification and physical tests still required

The final reports distinguish Blender topology checks from independent **STL-binary** checks. Tiny boolean slivers were cleaned at 0.001 mm tolerance, and mirrored normals were corrected. Confirm the latest `final_checks.json`: all delivered files should have zero boundary/nonmanifold edges, zero degenerate triangles and positive signed volume.

The mechanism was also swept at one-degree increments through keeper release and door opening, checking printed parts against fixed print geometry and the illustrative landing legs. This is sampled surface-intersection checking, not a continuous collision proof or a deformation/contact simulation. Metal pins, washers, springs, servo internals, wiring, cables under load and real petals require physical checks. Nominal wall/skin dimensions are design inputs, not a complete minimum-wall scan of every bolt ligament.

Before evaluating a flight installation:

- **Dimensional fit:** gauge every pin, eye, bolt, actuator and rail fit; check washer/nut access and full travel by hand.
- **Loaded retention:** support the assembly in a bench fixture with propellers removed. Load an actual 1 kg batch, hold it closed, inspect deflection and verify that both keepers and all pins remain secure. Establish proof loads with an engineer from the intended acceleration and material data.
- **Release reliability:** measure commanded-to-release time, current peaks, servo temperature, residual mass and any asymmetric opening. Repeat with dry and damp petals, partial/full fills and expected gentle motion. A useful initial screening is 20 successful bench releases; it is not a reliability qualification.
- **Reset/transport:** test manual reset, the two removable pins and cord routing after every cycle. Define and test loss-of-power behaviour.
- **Actual aircraft:** obtain frame mounting dimensions, permitted takeoff mass, motor/propeller/battery data, thrust margin, payload CG limits, controller/servo interface and real ground clearance. Include the entire attachment, hardware and modified landing gear in the load budget.

### Design references

Printing orientation and fit allowances must be adapted to the process; see [Prusa: Modeling with 3D printing in mind](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135).

Servo supply sizing must account for current demand rather than signal compatibility alone; see [Pololu: Electrical characteristics of servos](https://www.pololu.com/blog/16/electrical-characteristics-of-servos-and-introduction-to-the-servo-control-interface).
