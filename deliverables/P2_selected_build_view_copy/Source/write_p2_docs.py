from pathlib import Path
import json,csv,math
R=Path(__file__).resolve().parents[1]
R.joinpath('README.md').write_text('''# Dronetara P2 — selected aircraft + 1 kg petal-drop prototype

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
''')
R.joinpath('Electrical_and_Setup.md').write_text('''# P2 electrical architecture and bench setup

This is a connection plan, not a tested harness or a flight-ready parameter file. Use the official pinout for the delivered board revision and cable labels. Never infer pin order from connector shape or wire colour alone.

## Power

```text
12S standard LiPo (50.4 V full)
  -> factory high-current tails / SB175 main connector
  -> 125 V DC Class T main fuse in insulated holder
  -> PM08-CAN tinned-wire power module
  -> insulated star distribution
       -> four X6 Plus G2 integrated ESC/motor units
       -> UBEC 25A HV input -> 7.4 V dedicated servo power bus
PM08 regulated 5.3 V output -> Pixhawk POWER1
PM08 second regulated output -> POWER2 using official compatible harness
PM08 CAN -> Pixhawk CAN (correct termination and power/telemetry harness)
Pixhawk 5 V accessory output -> M10 GPS / RP3 receiver as appropriate
Pixhawk AUX1 signal + ground -> both servo signal inputs
```

The two PM08 outputs share one flight battery; they are not independent battery redundancy. Keep servo high-current returns on the BEC harness and join signal reference ground. **Do not connect the 7.4 V servo supply to the Pixhawk 5 V power or accessory input.** Do not feed BEC voltage back through a three-wire Y-lead into the autopilot: use signal/ground breakout and separate power injection.

The [PM08-CAN](https://holybro.com/products/dronecan-pm08-power-module-14s-200a) provides a published 200 A continuous rating and 5.3 V regulator outputs. Choose the tinned-wire variant to avoid a stock connector becoming the limiting component. Its short supplied 8 AWG leads are part of the manufacturer's rated module; retain them and use qualified crimped/busbar transitions, insulation and strain relief.

The selected [UBEC 25A HV](https://www.hobbywing.com/en/uploads/file/20221108/12f5024346c4952abc96da8c0f2ffc32.pdf) supports this input voltage and the two-servos' combined published stall demand of 10.4 A at 7.4 V. Use separate appropriately rated servo supply branches and short extensions at least as substantial as the servo's supplied 20 AWG cable. Measure actual connector and wire temperature under the release duty cycle. Supply capacity does not make sustained servo stall acceptable.

For the main connector select Anderson **SB175 blue 941 housing with 1382 1/0 AWG contacts**, matching both sides and professionally crimped short 1/0 AWG tails. Its current capability depends on contacts, cable, ambient temperature and tooling. It is not inherently an anti-spark connector. [Manufacturer datasheet](https://www.andersonpower.com/content/dam/ideal-anderson-power-dotcom/product-assets/default/data-sheets/DS-SB175.pdf)

The battery manufacturer must confirm that termination and its mass, insulation, strain relief and current capability. It is a custom procurement requirement; do not modify a live pouch pack or assume a smaller supplied plug is equivalent. Use an enclosed, professionally assembled precharge arrangement before main connection. A ground-only precharge fixture can use a 10-ohm, at least 500 W resistor bank and a momentary switch/fuse/wiring rated at least 63 V DC and 10 A. At 50.4 V its initial current/power are 5.04 A/254 W. Measure bus voltage; connect the main plug only when the voltage difference is below 2.5 V. If this cannot be achieved within the fixture's qualified duty, stop and resolve the load/circuit. Disconnect the ground fixture after main engagement. This proposed fixture has not been built or tested.

Select **Littelfuse JLLN200.X**, a 200 A Class T fuse with a 125 V DC rating and 20 kA DC interrupt rating, in a matched covered LFT30-series holder sized for 200 A. Confirm that the battery/harness prospective fault current is below that rating and coordinate the fuse curve with the actual conductors and holder temperature. This fuse is not an instantaneous 200 A motor-current limiter. The selected high interrupt rating avoids relying on a low-interrupt automotive fuse for the large LiPo source. [JLLN datasheet](https://www.littelfuse.com/assetdocs/jlln-datasheet?assetguid=3a7bc9bf-d932-4401-bdc7-b39f302195cf)

## Signals and control

| Function | Connection / configuration |
|---|---|
| Four motors | Pixhawk MAIN1–4 PWM signal and ground to corresponding integrated ESCs |
| Petal release | AUX1 / output 9 signal and ground to a powered two-servo breakout; mechanically index both keepers to move clear together |
| Receiver | RP3 TX to TELEM2 RX; RP3 RX to TELEM2 TX; regulated 5 V and ground |
| GPS/compass | Holybro M10 compatible GPS1 cable; verify connector version before power |
| Power telemetry | PM08 DroneCAN to a CAN port; configure sensor type and verify voltage/current against instruments |
| Ground setup | USB with propellers removed; install current stable ArduCopter supported by Pixhawk 6X |

For this model, front is **negative Y**, right is positive X. Standard ArduCopter Quad X mapping is MAIN1 front-right, MAIN2 rear-left, MAIN3 front-left, MAIN4 rear-right. Verify rotation against the current [official motor diagram](https://ardupilot.org/copter/docs/connect-escs-and-motors.html) and the installed CW/CCW props. Perform the software motor test with props removed; test order letters are not the same as output channel numbers.

The selected integrated ESC uses fixed PWM endpoints 1050–1950 μs; do not perform an unsupported endpoint calibration. Start with ordinary PWM, following its manual's startup/ramp recommendations. Verify that the controller's output logic level is accepted at the end of the actual harness; the Blender assembly does not establish electrical signal margins.

The [ArduPilot servo-gripper workflow](https://ardupilot.org/copter/docs/common-gripper-servo.html) uses `GRIP_ENABLE=1`, `GRIP_TYPE=1`, and `SERVO9_FUNCTION=28` for AUX1. Assign a deliberate RC switch, for example `RC8_OPTION=19`. Calibrate `GRIP_GRAB` and `GRIP_RELEASE` on the unloaded bench. Do not copy generic 1000/2000 μs values: the servos must achieve the required 90° without loading their stops. Use a servo-appropriate 50 Hz output group. Disable automatic closing because door raising is manual. Configure and test retention on RC loss rather than an automatic payload-release failsafe.

For CRSF on TELEM2 use `SERIAL2_PROTOCOL=23` when that connector maps to SERIAL2 on the selected board. Both TX and RX are required. Bind matching ELRS firmware/region and confirm channel ranges, link-loss behaviour and telemetry. [ArduPilot RC documentation](https://ardupilot.org/plane/docs/common-rc-systems.html)

Do not fly with these notes as a substitute for sensor calibration, motor order/rotation checks, controller tuning, verified failsafes, battery monitoring and a qualified load/current envelope. `MOT_BAT_CURR_MAX` is a delayed software control, not an instantaneous protective fuse. See [current limiting](https://ardupilot.org/copter/docs/current-limiting-and-voltage-scaling.html).

## Charging

Select **SkyRC PC1260 SK-100138** in standard 12S LiPo balance mode, using its correct 12S balance board and a professionally wired charge adapter. A charge-only XT90 adapter may be used at the charger's limited current; it must never be inserted into the flight power path. Start at 10 A, within the charger's published 12 A per-channel limit and below the battery's 1C rate. Verify cell count, lead polarity and all balance taps before connection. Never use a LiHV profile for the selected standard LiPo. [PC1260 manual](https://www.skyrc.com/download/PC1260_Instruction_Manual_EN_V1.0.pdf)
''')
# Preserve useful attachment counts while replacing superseded choices.
rows=list(csv.DictReader(R.joinpath('hardware_BOM.csv').open()))
rows=[x for x in rows if x['Item'] not in ['Return springs','Illustrative landing stand','Power supply and wiring']]
changes={
 'Rail clamp bolts':('16','M4 x 45 starting length; washers and locknuts','Includes P2 3 mm lower plate; verify actual stack'),
 'Servos':('2','Hitec D954SW at 7.4 V','Selected actuator; measure loaded release torque/current'),
 'Servo mounting screws':('8','M3 bolts with washers and locknuts; fit length','48 x 10 mm hole centres; horn-height spacers as required'),
 'Purchased servo horns':('2','Genuine compatible Hitec 25T double-arm metal horn','Choose opposed holes at radius 8–20 mm for slotted adapter; check supplied horn'),
 'Horn adapter screws':('4','M2.5 through-bolts with washers and locking nuts','One screw on each side of output; select length from actual horn stack'),
 'Mount rails':('2','Aluminium square tube 20 x 20 x 2 mm x 350 mm','M6 holes at +/-130 mm; four clamps match P2 lower plate'),
 'Suspension studs':('4','M6 x 136 mm','Nominal P2 geometry; verify nut/washer engagement before cutting')}
for x in rows:
 if x['Item'] in changes:x['Quantity'],x['Provisional size or interface'],x['Notes']=changes[x['Item']]
with R.joinpath('hardware_BOM.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
components=[
 ('Propulsion',4,'Hobbywing X6 Plus G2 with MFP24x8','2 CW + 2 CCW; 30 mm tube','2.992','Published total, four units','https://www.hobbywing.com/en/products/x6-plus-g2'),
 ('Flight battery',1,'Tattu standard LiPo 12S 22Ah 30C','Factory custom SB175 tails + matching 12S balance harness','4.650','Published +/-0.100 kg before custom-tail change','https://www.grepow.com/uav-battery/tattu-12s-lipo-drone-battery.html'),
 ('Controller',1,'Holybro Pixhawk 6X + standard baseboard','Use current matched board/cables','0.074','Published module+board estimate; harness additional','https://docs.holybro.com/autopilot/pixhawk-6x/technical-specification'),
 ('Power module',1,'Holybro PM08 CAN tinned-wire SKU15029','200 A module; official power/CAN harness','0.185','Published with cable','https://holybro.com/products/dronecan-pm08-power-module-14s-200a'),
 ('GPS',1,'Holybro M10 GPS SKU12040','Compatible 10-pin GPS1 cable','0.032','Published','https://holybro.com/products/m10-gps'),
 ('Receiver',1,'RadioMaster RP3 V2 ELRS 2.4 GHz','5 V CRSF; 2 antennas','0.0046','Published including antennas','https://www.radiomasterrc.com/products/rp3-expresslrs-2-4ghz-nano-receiver'),
 ('Transmitter',1,'RadioMaster Boxer ELRS 2.4 GHz','Matching region/firmware; ground equipment','','Not airborne','https://www.radiomasterrc.com/products/boxer-radio-controller-m2'),
 ('Release servo',2,'Hitec D954SW','7.4 V; matching 25T horns','0.132','Published excluding horns','https://www.hiteccs.com/public/uploads/data_sheet/HRC_D954SW_Specsheetv2.2_102-1729877827.pdf'),
 ('Servo BEC',1,'Hobbywing UBEC 25A HV','Set 7.4 V; separate servo power bus','0.074','Published','https://www.hobbywing.com/en/uploads/file/20221108/12f5024346c4952abc96da8c0f2ffc32.pdf'),
 ('Carbon arms',4,'Roll-wrapped 30 OD / 27 ID carbon tube','Start 515 mm nominal; trim only after pod fit','0.441','214 g/m source x 2.06 m','https://www.easycomposites.co.uk/30mm-roll-wrapped-carbon-fibre-tube-metric'),
 ('Centre plates',2,'Quasi-isotropic CFRP 3 mm sheet','400 x 400 mm; supplied DXFs','1.536','Solid bounding-volume estimate at assumed 1.6 g/cm3; subtract holes',''),
 ('Arm clamps',16,'Custom CNC 6061-T6 half clamps','8 complete split clamps; supplied dimensions','','CAD volume in mass report; not printable',''),
 ('Frame bolts',32,'M5 x 60 class 8.8 starting length','Washers and locking nuts; verify stack','','Included in frame hardware allowance',''),
 ('Landing frame',1,'Custom 6061-T6 tubular stand','20x2 struts/outriggers; 24x2 skids; saddle/gusset fit-up','','Included in landing allowance',''),
 ('Main connector',1,'Anderson SB175 mated pair','2 x blue 941 +4 x 1382 contacts; 1/0 AWG tails','','Included in electrical harness allowance','https://www.andersonpower.com/content/dam/ideal-anderson-power-dotcom/product-assets/default/data-sheets/DS-SB175.pdf'),
 ('Main fuse',1,'Littelfuse JLLN200.X','200 A /125 V DC; matching covered LFT30 holder','','Fault-current/thermal coordination required','https://www.littelfuse.com/assetdocs/jlln-datasheet?assetguid=3a7bc9bf-d932-4401-bdc7-b39f302195cf'),
 ('Power harness',1,'Qualified insulated star-distribution harness','>=200 A main path; short supplied ESC branches; branch/BEC protection','','See wiring document; verify duty and thermal limits',''),
 ('Precharge fixture',1,'Enclosed ground-only resistor/switch fixture','10 ohm >=500 W; switch/wire/fuse >=63 VDC 10 A','','Ground equipment; design/test required',''),
 ('Charger',1,'SkyRC PC1260 SK-100138','Standard 12S LiPo + correct balance board/charge adapter','','Ground equipment','https://www.skyrc.com/download/PC1260_Instruction_Manual_EN_V1.0.pdf'),
 ('Retention and mounts',1,'Battery pad, two straps, end restraint, avionics foam/straps','Secure cover and electrical cable strain relief','','Included in allowance','')]
with R.joinpath('Selected_components_BOM.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['System','Quantity','Selected component','Ordering/interface requirement','Total nominal mass kg','Mass basis / limitation','Primary source']);w.writerows(components)
R.joinpath('Fabrication/Cut_list.md').write_text('''# P2 nonprinted fabrication — mm

These are prototype manufacturing inputs, not released/certified structural drawings. Do not move these meshes into the printable parts folder.

- Two 400 × 400 × 3 mm quasi-isotropic CFRP plates. Lower bottom/top Z715/718; upper bottom/top Z760/763. Machine the corresponding DXFs, centered on X/Y zero. Hole JSON files give an independent circular-hole coordinate list. The upper plate also has four 28 ×4 mm rectangular strap slots centred at (±70, ±65), included in its DXF. Verify a 400 mm outside dimension after import; DXF is mm. Seal cut carbon edges and isolate galvanic contact with aluminium without silently changing the clamp stack.
- Four 30 OD /27 ID roll-wrapped carbon arms, nominal cut length 515 mm. Inner radius 110 mm, nominal outer radius 625 mm. Motor centres are radius 650 mm at ±45°/±135°: X/Y = ±459.619 mm. The last 25 mm centre offset is a packaging assumption, not a verified X6 pod dimension. Dry-fit actual pods, respect their specified full insertion and adjust tube length to motor centres before cutting. Follow manufacturer's clamp fastening procedure.
- Eight complete machined 6061-T6 split clamps: sixteen halves. Full envelope 30 mm radial ×54 mm tangential ×42 mm high, axis Z739; radial bore Ø30.10 mm; half-gap 0.40 mm before tightening. Each half is 20.80 mm high. Four Ø5.4 mm holes have radial/tangential centres ±8/±21 mm (16 ×42 pattern). Clamp centres at radius 130 and 210 mm on every arm. Meshes are local-axis machining references; dimensions here are authoritative. Tolerances must be set by the fabricator for the purchased carbon tube, surface finish and grip trial. Inspect tube crush/slip; no torque has been qualified.
- Thirty-two M5 through-bolts, nominal 60 mm, with washers and locknuts. Verify stack and thread protrusion. The same four bolts join top plate, upper clamp, lower clamp and bottom plate at each station.
- Lower plate has sixteen Ø4.4 mm hopper-mount holes, arranged on four 38 ×20 mm patterns centered at (±120, ±70). These match the upper halves of the printed rail clamps.
- Landing saddle pairs: Ø5.4 mm at X = ±175 ±12, Y = ±130. Four 40 ×24 ×6 mm aluminium saddle plates, top Z715. Two holes in each on a 24 mm line. Eight M5 bolts with washers/locknuts; choose length from physical stack.
- Four 20 OD ×2 mm wall aluminium outriggers: from (±175, ±130,680) to (±260, ±220,680), approximately 123.794 mm centreline. Four same-section main legs: (±260,±220,680) to (±290,±245,40), approximately 641.190 mm centreline. Four vertical saddle drops: 29 mm nominal centreline. Two 24 OD ×2 mm wall skids: X±290, Y−300 to+300, Z30; 600 mm each. Coordinate signs pair consistently within each corner. Miter/cope and end fit change raw cut lengths. Landing pads are nonprinted elastomer.
- The landing joints need actual saddle/gusset/weld design and allowance for 6061 weld heat effects; reference intersecting tubes do not constitute a joint detail. A fabricator must resolve joints and qualify landing loads before flight. This is an explicit remaining engineering interface.
- Hopper rails: two 20 ×20 ×2 mm aluminium square tubes, 350 mm long, with Ø6.6 mm suspension holes at longitudinal ±130 mm. Four M6 studs, nominal 136 mm, adjust only for actual washer/nut engagement.

Structural adhesives, printed substitutes, unsupported welded joints and guessed carbon-clamp torque are not specified as load-rated solutions. The Blender model establishes packaging and assembly interfaces; real material data and proof tests establish capability.
''')
fields=['Test','Required observation / acceptance basis','Measured result','Pass/fail','Date','Operator']
checks=[
 ('Petal capacity','1.000 kg of representative loosest petals fits below fill line with cover; record volume and density'),
 ('Printed dimensions','Gauge hinges, slots, holes and interface clearances; no forced fit'),
 ('Actual mass','Weigh complete ready-to-fly system including 1 kg petals; <=21 kg sizing ceiling, recalculate if exceeded'),
 ('CG before/after release','Record X/Y/Z CG with full and empty hopper; verify controller/frame limits'),
 ('Structural load','Engineer establishes proof load and allowable deflection from materials and intended acceleration/landing loads; record no slip/cracking/permanent deformation'),
 ('Door retention','Full petal batch remains retained, pins/keepers secure and no progressive creep'),
 ('Release torque','Measure each keeper worst-case release torque; demonstrate chosen actuator duty margin, not just stall rating'),
 ('Release screening','At least 20 screening cycles with dry/damp full/partial batches; record timing, current, temperature and residual mass each time'),
 ('Cord routing','No snagging; 95-degree nominal stop and secure anchors; test opening shock'),
 ('RC/power loss','No unintended drop or uncontrolled motor operation in defined failsafe tests'),
 ('Electrical build','Confirm pinouts, polarity, precharge, insulation, fuse fault rating and power separation'),
 ('Motor test','Props removed: validate motor order, direction, PWM endpoints, startup delay and failsafe'),
 ('Restrained propulsion','Measured bus <=100 A continuous and selected temporary burst envelope; temperatures within manufacturer limits; verify full-charge current cap'),
 ('Thrust reserve','Measure at least 1.8 x actual AUW transient thrust in qualified short burst envelope; sustained hover with thermal margin'),
 ('Flight evaluation','Progressive controlled tests only after preceding acceptance; record stability, reserve, vibration and post-release response')]
with R.joinpath('Qualification.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(fields)
 for a,b in checks:w.writerow([a,b,'NOT TESTED','','',''])
print('P2_DOCS_WRITTEN')
