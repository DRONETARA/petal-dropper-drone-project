# Dronetara P2 — selected aircraft + 1 kg petal-drop prototype

The design target is **at least 1 kg of flower petals alone**. The aircraft, battery, hopper and hardware are additional mass. This package chooses the aircraft and electronics from scratch; it does not require an existing drone.

P2 contains an editable Blender assembly, 46 individual printable attachment parts, a proposed carbon/aluminium airframe, plate machining files, component BOM, wiring plan and qualification worksheet. It is a **digital engineering prototype**. No parts have been printed, weighed, load-tested or flown, and no physical petal-release test has been performed. The 1 kg capacity remains conditional on actual petal volume and structural/release tests.

## Chosen build

- Custom Quad X, 1,300 mm diagonal motor spacing, four 30 mm carbon-tube arms and two 400 × 400 × 3 mm carbon-sheet centre plates. Machined aluminium split clamps carry arm loads; these are not printable parts.
- Four **Hobbywing X6 Plus G2** integrated propulsion units with genuine **MFP24×8** props, two CW and two CCW. The clearance model uses the published 620 mm prop span. The 30 mm tube interface is sourced; the detailed pod shape and tube insertion offset remain reference envelopes. Trim arms to obtain the specified motor centres using the actual units. [Manufacturer](https://www.hobbywing.com/en/products/x6-plus-g2)
- **Tattu standard LiPo 12S 22 Ah 30C**, not a LiHV or semi-solid substitute. Request the specified high-current power termination and a balance harness compatible with the charger; this is a supplier configuration, not a verified stocked SKU. [Battery family](https://www.grepow.com/uav-battery/tattu-12s-lipo-drone-battery.html)
- **Holybro Pixhawk 6X**, **PM08-CAN tinned-wire power module**, **M10 GPS**, and **RadioMaster RP3 V2 ELRS 2.4 GHz** receiver with an ELRS transmitter.
- Two **Hitec D954SW** release servos, genuine matching 25T horns, and **Hobbywing UBEC 25A HV set to 7.4 V**. Corrected carriers use the manufacturer's 48 × 10 mm mounting centres and shaft-relative offsets. The slotted adapters avoid inventing a printable servo spline. Horn fit still needs a bench check.

The conservative design ceiling is **21 kg all-up** for this prototype. It is a sizing assumption, not a certified maximum takeoff weight. Read `Mass_and_Performance.md` for the mass budget, hover estimate and operating limits.

## Files

| File/folder | Use |
|---|---|
| `PetalDrop_1kg_Assembly.blend` | Complete editable P2 drone and attachment; mm scene; named collections |
| `STL_mm/` | 46 separate printable attachment pieces; one of each filename |
| `parts_manifest.csv` / `.json` | Individual dimensions, print notes and solid PETG estimates |
| `Fabrication/` | Nonprinted plate DXFs, hole coordinates, machined clamp references and cut list |
| `Selected_components_BOM.csv` | Aircraft, electronics and ground-equipment selection |
| `hardware_BOM.csv` | Attachment screws, pins, washers, cords and rails |
| `Electrical_and_Setup.md` | Supply separation, signal connections and bench setup |
| `Mass_and_Performance.md` | Reproducible analytical sizing, assumptions clearly separated from measurements |
| `Qualification.csv` | Blank physical acceptance records; no fabricated pass results |
| `final_checks.json` | Independent exported-STL checks and sampled mechanism sweep |
| `Assembly_closed.png`, `Assembly_open.png`, `Mechanism_open.png` | Closed, discharge and underside views |

The original starter and P1 package remain preserved in the parent output folder. Use P2 files together; do not mix the earlier servo carriers or horn adapters into this build. Blender geometry is editable mesh geometry, not a parametric STEP assembly. Procedural source scripts are included in `Source/` for review and adaptation.

## Capacity and release mechanism

The hopper has a 320 × 320 mm interior, a fill datum at Z570 mm, and approximately **22.12 litres** below that line before hardware displacement. The geometric requirement for 1 kg is a loose bulk density of at least **45.21 kg/m³**; actual usable volume is slightly less. No universal petal density is assumed. Weigh and loosely fill representative dry and damp batches. If a full 1 kg batch does not fit below the line with its cover, the hopper must be enlarged and rechecked.

Two ribbed doors form the bottom. Each of two keeper dogs supports the inner edges of both doors. The load travels through the dog, thrust washer and carrier shelf into the hopper; the servo rotates a separate steel spindle. Hinges carry part of the door load. The doors open by gravity after the keepers rotate 90 degrees. Four adjustable cords limit opening to a nominal 95 degrees. The broad 292 × 292 mm throat helps release, but does not prove that wet or tangled petals cannot bridge.

**Reset is manual.** Raise and support the empty doors, return both keepers, then insert both 3 mm transport pins. Remove both pins before commanding release. The P1 unengineered spring illustrations have been removed. With transport pins removed there is no demonstrated power-loss retention mechanism; friction and servo gearing are not a qualified mechanical lock.

| Timeline frame | Operation |
|---|---|
| 1 | Closed, transport pins installed |
| 20 | Pins removed |
| 20–50 | Keepers rotate clear |
| 50–90 | Gravity door opening to cord limit |
| 90–105 | Open discharge state |
| 105–125 | Manual empty-door lifting, illustrated with keyframes |
| 125–155 | Keeper return under supported doors |
| 180 | Pins reinstalled |

Animation illustrates the sequence; it is not a physics simulation or flight-control program.

## Printing and mechanical assembly

Import STLs as **millimetres at 100% scale**. Each exported part fits a 220 mm cube. Export orientation places its bounding box on the bed; choose final support and layer orientation in the slicer. The starting geometry has 2.4 mm hopper walls/door skins, 4 mm hopper flanges, 0.4 mm module seams, 5.4 mm hinge bores for 5 mm pins, and typical 4.4 mm M4 holes. These are nominal design dimensions, not measured printer tolerances.

Use a calibrated material profile, initially a 0.4 mm nozzle and 0.2 mm layers. Slice and weigh a hinge, carrier and suspension bracket first. PETG density of 1.27 g/cm³ is only the planning assumption used in the manifest. Wall count, infill and layer direction need material/process testing; no infill percentage guarantees payload strength.

1. Bolt the eight corner modules together using wide washers and locknuts. Keep seams even and seal externally. Install the eight throat rails, four hinge clevises and four suspension brackets.
2. Join each pair of door tiles using two underside splice plates. Fit four steel hinge pins, thrust washers and positive end retention. Confirm free travel by hand.
3. Install the two corrected D954SW carriers, thrust washers, steel spindles and keeper dogs. The ear support is Z290.8 mm; output height is based on the drawing. Actual grommets and horn thickness may require spacers. Check the 6 mm spindle axis is concentric with the servo output and does not force an axial load into the servo.
4. Bolt each slotted adapter to a genuine compatible 25T double-arm horn with two opposed M2.5 through-bolts and washers. The slots accept hole radii of 8–20 mm. This is an adjustable interface, not a claim that every supplied horn has that pattern. Select a horn with two suitable holes, or drill an appropriate metal horn using its supplier's limits. Do not substitute a printed spline or rely on adhesive. Check screw access and the full rotation before fastening the spindle cross-bolts.
5. Fit eight M4 eye bolts and four nonprinted cords. Set nominal eye-centre lengths to **113.946 mm at the 95° open position**, then adjust for actual eye geometry, knots and stretch. The provisional selection target is at least 100 N working load per cord; anchor strength and opening shock require testing. Keep slack cords out of the latch path.
6. Install four M6 studs and two 20 × 20 × 2 mm aluminium rails. Four split rail clamps attach to the matching M4 hole sets in the lower carbon plate. Top clamp faces meet Z715. Use the P2 plate DXF; this interface is now designed into the chosen frame.
7. Assemble the carbon plates, eight machined split arm-clamp assemblies and carbon tubes. Follow `Fabrication/Cut_list.md`. Carbon clamping torque is not established; qualify slip resistance without crushing/delaminating the tube. Do not treat the reference pod envelope as a drilling template.
8. Fit the fabricated tubular landing stand. The outriggers run below the carbon arms, leaving the door sweep clear. Weld/gusset design, heat-affected material strength and landing-load qualification are still fabrication engineering work.
9. Secure the battery with a resilient pad, two independent webbing straps and end restraint. Retain the controller on vibration-isolating foam with straps; provide connector access. Secure all electronics, the fabric petal cover and cable slack.

Lengths in the fastener BOM are starting selections. Verify stack thickness, washer access, full locknut engagement and no projecting threads in the petal path. All primary aircraft structure is purchased carbon or fabricated metal. Do not print props, motor clamps or structural plate substitutes.

## What the digital checks establish

`final_checks.json` validates the actual binary STLs, separately from Blender's in-memory meshes. It also samples keeper motion from 0–90° and doors from 0–95° in 1° increments against fixed printable parts and landing references. Zero reported surface intersections is not continuous collision proof: contact/deformation, hardware interiors, wires, flexible cords, petals and aerodynamics are outside that check. Exact seating contacts, supplied horn details and fastening remain physical checks.

The frame and component envelopes are for a reviewable prototype build. The plate mounting patterns and printable mechanism are modeled, but motor-pod internals, welded landing joints, battery termination and horn stack are not production-qualified interfaces. No FEA, material coupon test, fatigue assessment, thrust-stand test or reliability demonstration is represented as complete.

Use `Qualification.csv` to record actual results. Start with the stationary mechanism and propellers removed. Confirm fit, weigh the assembly, retain a real 1 kg batch, measure loaded release torque/current, test at least 20 screening cycles across representative petals, and record residual mass. Establish structural proof loads from intended manoeuvre/landing loads and real material data. Then qualify the complete electrical installation and propulsion in a restrained test fixture before progressive flight tests at an appropriate clear test site. A 20-cycle screen is not a reliability certification.
