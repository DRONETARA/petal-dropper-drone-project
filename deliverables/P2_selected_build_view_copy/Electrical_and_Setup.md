# P2 electrical architecture and bench setup

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
