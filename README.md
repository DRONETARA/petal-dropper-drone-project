# Petal Dropper Drone Project

This repository contains the complete Blender design package for Dronetara's flower-petal dropper drone. The current deliverable is P2: a selected-aircraft digital prototype with a 1 kg flower-petal target.

Start here:

- `deliverables/P2_selected_build/PetalDrop_1kg_Assembly.blend` is the editable P2 assembly in millimetres.
- `deliverables/P2_selected_build/STL_mm/` contains 46 individual printable attachment parts. Import at 100% in millimetres.
- `deliverables/P2_selected_build/README.md` is the build and assembly guide.
- `deliverables/P2_selected_build/Selected_components_BOM.csv`, `Electrical_and_Setup.md`, `Mass_and_Performance.md`, and `Fabrication/` contain the component selection, wiring approach, sizing, DXFs, and machining references.
- `deliverables/flap_opening_animation/PetalDrop_Flaps_Opening.mp4` is an 8.13-second close-up of the keeper release and flap opening. `PetalDrop_Flap_Opening_Review.blend` is the editable animation review scene; press Space in Blender to play it.

P2 selects a 1,300 mm Quad X with four Hobbywing X6 Plus G2 propulsion units, a Tattu 12S 22 Ah battery, Pixhawk 6X, PM08-CAN power module, M10 GPS, ELRS receiver, and two Hitec D954SW release servos. The package also retains the original starter assembly and P1 attachment prototype under `deliverables/`.

The design is a digital prototype, not a flight-ready aircraft. It targets 1 kg of petals, and its planning mass is about 20.3 kg including the target petals and contingency. Actual petal capacity, printed-part strength, release reliability, electronics, propulsion, landing structure, and flight performance are untested. The P2 qualification worksheet records the physical tests still required.

`packages/Dronetara_P2_Selected_Build.zip` is the standalone P2 handoff archive. `source/` retains the useful generation scripts, while P2's portable regeneration sources are also inside `deliverables/P2_selected_build/Source/`.

## Repository layout

| Path | Contents |
| --- | --- |
| `deliverables/Dronetara_Starter.blend` | Original editable starter drone |
| `deliverables/P1_attachment_prototype/` | Earlier P1 attachment, STL set, checks, and preview renders |
| `deliverables/P2_selected_build/` | Current selected-aircraft build package and 46-printable-part STL set |
| `deliverables/P2_selected_build_view_copy/` | Preserved alternate P2 Blender view copy; use the P2 build folder as canonical documentation |
| `deliverables/flap_opening_animation/` | Opening animation MP4, review Blender file, source frames, and verification notes |
| `packages/` | Portable P2 ZIP handoff |
| `source/` | Historical generation scripts used to create the project assets |
