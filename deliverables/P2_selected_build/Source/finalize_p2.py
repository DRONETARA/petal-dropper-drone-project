import bpy,bmesh,json,math,csv
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'PetalDrop_1kg_Assembly.blend'))
g={}
for o in bpy.data.objects:
 if o.type=='MESH' and (o.name.startswith('MACHINED') or o.name in ['Upper_frame_plate','Lower_frame_plate'] or o.name.startswith('UNVERIFIED')):
  bm=bmesh.new();bm.from_mesh(o.data);v=abs(bm.calc_volume());bm.free();k='Clamps' if o.name.startswith('MACHINED') else 'Landing' if o.name.startswith('UNVERIFIED') else 'Plates';g[k]=g.get(k,0)+v*(1.6 if k=='Plates' else 2.7)/1e6
pm=json.load(open(R/'parts_manifest.json'));printed=sum(x['solid_PETG_mass_g'] for x in pm)/1000
items=[('Printed attachment',printed,'CAD solid volume; assumed PETG 1.27 g/cm3'),('Attachment rails/fasteners/cords/cover/horns',1.0,'Planning allowance, excludes servos'),('Two release servos',.132,'Published, excluding horns'),('Four propulsion units',2.992,'Published with props and cables'),('Battery',4.65,'Published nominal; custom-tail difference in harness allowance'),('Carbon centre plates',g['Plates'],'CAD volume; assumed CFRP 1.6 g/cm3'),('Machined arm clamps',g['Clamps'],'CAD volume; assumed aluminium 2.7 g/cm3'),('Carbon arms',.214*2.06,'Supplier linear mass x nominal tube length'),('Tubular landing members',g['Landing'],'CAD volume; assumed aluminium 2.7 g/cm3'),('Landing saddles/gussets/pads',.2,'Allowance beyond tubular members'),('Aircraft fasteners',.55,'Allowance including washers, nuts and mounting bolts'),('FC/PM/GPS/RX/BEC',.074+.185+.032+.0046+.074,'Published component masses, approximate'),('Power distribution, fuse, connector, added wiring',.65,'Allowance; weigh custom harness'),('Straps/foam/avionics supports',.18,'Allowance'),('Petals',1.0,'Required payload alone'),('Unallocated mass contingency',.5,'Planning reserve')]
total=sum(x[1] for x in items)
assert total<21,(total,g)
# Interpolate manufacturer 46 V bench data at the conservative design ceiling.
i=12.4+(5250-4712)/(5256-4712)*(14.7-12.4);p=46*4*i;usable=976.8*.75;mission_p=p*1.15+20;duration=60*usable/mission_p
calc={'mass_items':[dict(item=a,kg=round(b,4),basis=c) for a,b,c in items],'planning_total_kg':round(total,3),'design_ceiling_kg':21,'unallocated_within_ceiling_kg':round(21-total,3),'hover_thrust_per_motor_g':5250,'bench_interpolated_bus_A_at46V':round(4*i,2),'bench_hover_W':round(p,1),'planning_hover_W_with15pct_and20W_allowance':round(mission_p,1),'usable_energy_Wh_75pct':usable,'analytical_hover_minutes':round(duration,1),'nominal_motor_radius_mm':650,'motor_diagonal_mm':1300,'adjacent_motor_mm':round(650*math.sqrt(2),3),'prop_span_mm':620,'nominal_adjacent_prop_gap_mm':round(650*math.sqrt(2)-620,3),'data_status':'Estimates and manufacturer laboratory data, not measured aircraft performance'}
json.dump(calc,open(R/'sizing.json','w'),indent=2)
with open(R/'Mass_budget.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['Item','Planning mass kg','Basis']);w.writerows(items);w.writerow(['TOTAL',round(total,3),'Includes 1 kg petals and 0.5 kg contingency'])
text=f'''# P2 mass and performance sizing

The planning total is **{total:.2f} kg**, including **1.000 kg of petals** and 0.500 kg of contingency. The design ceiling is 21 kg, leaving another {21-total:.2f} kg before that ceiling. This is not weighed mass or an approved takeoff limit. See `Mass_budget.csv` and `sizing.json` for reproducible inputs.

| Item | kg | Basis |
|---|---:|---|
'''+''.join(f'| {a} | {b:.3f} | {c} |\n' for a,b,c in items)+f'''
Thin printed walls remain largely solid regardless of infill. Do not subtract a guessed infill percentage from the whole attachment. Actual fasteners, battery termination, weld gussets, supports and wire routing may exceed their allowances. Weigh the complete aircraft after assembly; if it exceeds 21 kg, reduce mass or resize/requalify the propulsion.

## Lift and current

At 21 kg, hover requires 5.25 kg thrust per motor. Interpolation between the manufacturer's 46 V laboratory points (4,712 g at 12.4 A and 5,256 g at 14.7 A) gives approximately **{4*i:.1f} A total / {p/1000:.2f} kW**. This is a static sea-level estimate at the cited test conditions, not a flight measurement. The manufacturer's recommended 4–6 kg-per-axis range supports choosing this motor family. [Hobbywing X6 Plus G2](https://www.hobbywing.com/en/products/x6-plus-g2)

The published maximum 12.526 kg per unit would total 50.104 kg and a 2.39:1 ratio at 21 kg, but that maximum is outside the proposed routine electrical envelope and cannot be treated as continuous thrust. The integrated ESC's 25 A continuous rating limits four-unit continuous current to 100 A before accessory allowance; individual motor currents must also remain within their ratings. PM08's 200 A rating is not the motor limit.

For initial qualification, target at most **160 A bus for a maximum two-second transient**, below 100 A total propulsion current continuously, and verify each ESC separately. A preliminary command ceiling near the 78% laboratory point corresponds to 156.8 A and 39.144 kg total static thrust at 46 V, or 1.86:1 at 21 kg. Percent bench throttle is not guaranteed to map exactly to an autopilot parameter. Establish the actual PWM ceiling with current/thrust measurements at a full 50.4 V battery before flight. Servo/accessory current also belongs in the bus total.

A hypothetical 20% thrust derating reduces that transient figure to 31.315 kg, only 1.49:1 at 21 kg. To retain a 1.8:1 transient ratio in that scenario, mass would need to be at most 17.40 kg. Therefore this selection does **not** establish hot/high-altitude performance; qualify the intended environment or revise mass/propulsion. Software current limiting reacts too slowly to substitute for electrical sizing.

## Endurance and geometry

The standard 12S 22 Ah pack is nominally 976.8 Wh. Reserving 25% energy and adding 15% to the bench hover power plus 20 W for electronics gives approximately **{duration:.1f} minutes of analytical hover** at the 21 kg ceiling. Wind, manoeuvres, voltage sag, temperature, battery ageing and reserve policy change this. It is not a promised flight duration. [Battery specification](https://www.grepow.com/uav-battery/tattu-12s-lipo-drone-battery.html)

Adjacent motor centres are {650*math.sqrt(2):.2f} mm apart. A nominal 620 mm swept diameter leaves {650*math.sqrt(2)-620:.2f} mm between adjacent rotor disks in plan. The detailed pod outline is approximate; confirm actual insertion and final rotor centres. Battery and GPS envelopes lie inside the central clear region. The mechanism's sampled minimum door-ground gap is recorded independently in `final_checks.json`; do not confuse it with clearance under pitch/roll or uneven ground.

The centered battery and hopper support a roughly centered plan CG, but hardware distribution and departing petals change it. Measure full/empty CG and recheck stability; no inertia model or autopilot tuning was completed.

## Release actuator and structure

The selected D954SW at 7.4 V has published 29 kgf·cm stall torque (2.844 N·m), 5.8 kgf·cm peak-efficiency torque (0.569 N·m), and 5.2 A stall current. Neither torque number is a continuous application rating. [Hitec drawing/data](https://www.hiteccs.com/public/uploads/data_sheet/HRC_D954SW_Specsheetv2.2_102-1729877827.pdf)

An intentionally conservative friction estimate of 0.4 × (1.7 kg ×9.81) ×0.060 m is 0.400 N·m if one keeper briefly carries that whole load. Real hinge load sharing may lower it; petal snagging may raise it. A threefold design target would require 1.20 N·m of verified short-duration output at the actual voltage/duty, not merely a larger stall number. This has not been demonstrated. Measure breakaway torque and actual loaded release current/temperature; change the actuator or bearing/contact design if margin is insufficient.

For a provisional 3g sizing case, a 21 kg aircraft corresponds to 618 N overall. An attachment around 6 kg corresponds to 177 N, nominally 44 N per suspension point under ideal sharing. Unequal load distribution, landing shocks, creep and layer adhesion invalidate treating those as certified loads. The frame/printed mounts still require engineering proof loads based on actual material properties and intended use. CAD topology and absence of sampled collision do not establish strength.
'''
R.joinpath('Mass_and_Performance.md').write_text(text)
for name,fn in [('READ ME • prototype limitations','README.md'),('P2 • Electrical and setup','Electrical_and_Setup.md'),('P2 • Mass and performance','Mass_and_Performance.md'),('P2 • Fabrication','Fabrication/Cut_list.md')]:
 t=bpy.data.texts.get(name) or bpy.data.texts.new(name);t.clear();t.write(R.joinpath(fn).read_text())
# Remove inherited P1 verification conclusions. Keep current standalone checks as authoritative.
vr=json.load(open(R/'verification.json'));vr['revision']='P2';vr['solid_PETG_total_kg']=round(printed,3);vr['authoritative_motion_and_STL_report']='final_checks.json';vr['aircraft_sizing_report']='sizing.json';json.dump(vr,open(R/'verification.json','w'),indent=2)
bpy.context.scene['Design_AUW_ceiling_kg']=21.;bpy.context.scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(R/'PetalDrop_1kg_Assembly.blend'))
print('FINAL_MASS',round(total,3),g,flush=True)
