import bpy,bmesh,math,json,os,shutil
from mathutils import Vector,Matrix
from pathlib import Path
BASE=str(Path(__file__).resolve().parents[1])
OLD=str(Path(__file__).resolve().parent/'P1_base');OUT=BASE
os.makedirs(OUT+'/STL_mm',exist_ok=True);os.makedirs(OUT+'/Fabrication',exist_ok=True)
for f in ['parts_manifest.json','verification.json','limit_cords.json','hardware_BOM.csv','README.md']:
 shutil.copy2(OLD+'/'+f,OUT+'/'+f)
bpy.ops.wm.open_mainfile(filepath=OLD+'/PetalDrop_1kg_Assembly.blend');sc=bpy.context.scene;sc.frame_set(1)
for c in list(bpy.data.collections):
 if c.name[:2] in ['01','02','03','04','05','06','07']:
  for o in list(c.objects):bpy.data.objects.remove(o,do_unlink=True)
  bpy.data.collections.remove(c)
for o in list(bpy.data.objects):
 if any(s in o.name for s in ['SERVO PLACEHOLDER','Servo mounting ear envelope','CLOSED-BIAS SPRING']):bpy.data.objects.remove(o,do_unlink=True)
COL=None

def col(n):
 global COL
 COL=bpy.data.collections.get(n) or bpy.data.collections.new(n)
 if COL.name not in sc.collection.children:sc.collection.children.link(COL)
 return COL

def own(o):
 for c in list(o.users_collection):c.objects.unlink(o)
 COL.objects.link(o);return o

def mat(n,c,m=0):
 x=bpy.data.materials.new(n);x.diffuse_color=(*c,1);x.use_nodes=True;p=x.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=m;p.inputs['Roughness'].default_value=.36;return x
carbon=mat('P2 carbon tube and sheet',(.035,.05,.065),.35);metal=mat('P2 machined aluminium',(.38,.44,.49),.8);orange=mat('P2 orange identification',(.95,.22,.025),.1);blue=mat('P2 purchased electronics',(.06,.15,.25),.3);black=bpy.data.materials['Prototype • graphite brackets'];accent=bpy.data.materials['Prototype • safety orange']

def cube(p,d):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=own(bpy.context.object);o.dimensions=d;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return o

def cyl(p,r,h,axis='Z',n=48):
 bpy.ops.mesh.primitive_cylinder_add(vertices=n,radius=r,depth=h,location=p);o=own(bpy.context.object)
 if axis=='X':o.rotation_euler.y=math.pi/2
 if axis=='Y':o.rotation_euler.x=math.pi/2
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);return o

def boolean(a,b,op='DIFFERENCE'):
 bpy.context.view_layer.objects.active=a;m=a.modifiers.new(op,'BOOLEAN');m.operation=op;m.solver='EXACT';m.object=b;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(b,do_unlink=True);return a

def union(ps):
 a=ps[0]
 for b in ps[1:]:boolean(a,b,'UNION')
 return a

def hole(o,p,r,h,axis='Z'):boolean(o,cyl(p,r,h,axis))

def hard(o,n,m=metal,note='Designed fabrication geometry; physical qualification pending'):
 o.name=n;o.data.materials.clear();o.data.materials.append(m);o['Manufacture']='NONPRINTED';o['Notes']=note;return o

def beam(n,a,b,r,m=carbon,inner=0):
 a,b=Vector(a),Vector(b);o=cyl((a+b)/2,r,(b-a).length)
 if inner:boolean(o,cyl((a+b)/2,inner,(b-a).length+2))
 o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return hard(o,n,m)

def meshreplace(old,new,note):
 new.matrix_world=Matrix.Identity(4)@new.matrix_world
 # Transfer replacement world coordinates to the original animated object's local coordinates.
 new.data.transform(old.matrix_world.inverted()@new.matrix_world);new.data.materials.clear();[new.data.materials.append(m) for m in old.data.materials];old.data=new.data.copy();old['Notes']=note;bpy.data.objects.remove(new,do_unlink=True)
manifest=json.load(open(OUT+'/parts_manifest.json'));rows={x['part']:x for x in manifest}
col('13 • PRINT | servo-release keepers')
for sy in [-1,1]:
 y=sy*200
 chunks=[cube((0,sy*196,322.5),(170,64,8)),cube((0,sy*166.4,374),(170,8,44))]
 for x in [-81,81]:chunks.append(cube((x,sy*193,353),(8,58,69)))
 chunks += [cube((-10,y,288.3),(86,36,5)),cube((-54,y,304.4),(8,36,35.2)),cube((34,y,304.4),(8,36,35.2))]
 q=union(chunks)
 for x in [-81,81]:boolean(q,cube((x,sy*195,356),(14,30,32)))
 for x in [-53,53]:boolean(q,cube((x,sy*198,322.5),(30,30,16)))
 boolean(q,cube((0,sy*166.4,374),(110,20,24)));boolean(q,cube((-10,y,288.3),(42,22,16)))
 hole(q,(0,y,322.5),3.4,20);hole(q,(20,sy*180,322.5),1.7,20)
 for x in [-34,14]:
  for dy in [-5,5]:hole(q,(x,y+dy,288.3),1.7,14)
 for x in [-80,-65,65,80]:
  for z in [364,386]:hole(q,(x,sy*166.4,z),2.2,20,'Y')
 for x in [-72,72]:hole(q,(x,sy*175,322.5),2.2,25)
 name=f'Servo_keeper_carrier_{sy:+d}';note='P2 Hitec D954SW: mounting centres 48 x 10 mm, output-axis offsets -34/+14 mm. Ear support Z290.8; fit grommets/spacers to actual horn height. M3 bolts with washers. Shelf carries spindle thrust.'
 meshreplace(bpy.data.objects[name],q,note);rows[name]['notes']=note
 # Slotted horn adaptor: no invented spline. Actual 25T purchased horn remains mandatory.
 q=union([cube((0,y,307),(46,10,5)),cyl((0,y,312),8,10)])
 hole(q,(0,y,312),3.3,25);hole(q,(0,y,313),1.7,24,'X')
 for sx in [-1,1]:
  cut=union([cube((sx*14,y,307),(12,2.8,10)),cyl((sx*8,y,307),1.4,10),cyl((sx*20,y,307),1.4,10)])
  boolean(q,cut)
 old=f'Horn_adapter_PROVISIONAL_{sy:+d}';new=f'H25T_slotted_horn_adapter_{sy:+d}'
 note='P2: purchased Hitec 25T double-arm horn; two opposed 2.8 mm slots spanning radii 8–20 mm. M2.5 through-bolts and washers; check horn hole availability and clearance at bench. No printed servo spline. 6 mm steel spindle/M3 cross-bolt.'
 o=bpy.data.objects[old];meshreplace(o,q,note);o.name=new;row=rows.pop(old);row.update(part=new,file=new+'.stl',notes=note);rows[new]=row
 hard(cube((-10,y,282.8),(40,20,37)),f'Hitec D954SW servo {sy:+d}',blue,'Manufacturer body envelope; mounting ears and horn height per drawing, final grommet stack to fit.')
 hard(cube((-10,y,292.05),(53,20,2.5)),f'D954SW mounting ears {sy:+d}',blue)
 # Horn thin reference has clearance above the servo; supplier screw positions must fit adapter slots.
 horn=hard(cube((0,y,303.65),(44,7,1.7)),f'Purchased Hitec 25T horn {sy:+d}',metal,'REFERENCE envelope, supplied horn shape/hole positions require fit check. Slots accept opposed holes at radius 8–20 mm.')
 piv=bpy.data.objects['Front keeper • servo 1' if sy<0 else 'Rear keeper • servo 2'];w=horn.matrix_world.copy();horn.parent=piv;horn.matrix_world=w
for o in bpy.data.objects:
 if o.name.startswith('Rail_clamp_upper'):
  o['Notes']='P2 matching holes in lower frame plate: M4 on 38 x 20 mm centres; clamp top Z715.';rows[o.name]['notes']=o['Notes']
# Real proposed airframe. All primary frame members are carbon or metal, not printed.
col('01 • P2 custom carbon frame | NONPRINT')
plateholes=[]
for sx in [-1,1]:
 for sy in [-1,1]:
  a=math.atan2(sy,sx)
  for r in [130,210]:
   for u in [-8,8]:
    for v in [-21,21]:plateholes.append(((r+u)*math.cos(a)-v*math.sin(a),(r+u)*math.sin(a)+v*math.cos(a),2.7,'M5 arm clamp'))
railholes=[(sx*120+dx,sy*70+dy,2.2,'M4 hopper rail') for sx in [-1,1] for sy in [-1,1] for dx in [-19,19] for dy in [-10,10]]
# Landing outrigger attachment holes at x +/-120, y +/-150. M5 pair through saddle plate.
leg_holes=[(sx*175+dx,sy*130,2.7,'M5 landing saddle') for sx in [-1,1] for sy in [-1,1] for dx in [-12,12]]
for name,z,holes in [('Lower_frame_plate',716.5,plateholes+railholes+leg_holes),('Upper_frame_plate',761.5,plateholes)]:
 q=cube((0,0,z),(400,400,3))
 for x,y,r,_ in holes:hole(q,(x,y,z),r,12)
 if name=='Upper_frame_plate':
  for x in [-70,70]:
   for y in [-65,65]:boolean(q,cube((x,y,z),(28,4,12)))
 hard(q,name,carbon,'Machine 3 mm quasi-isotropic CFRP sheet, 400 x 400. Hole DXF included; structural strength not established by CAD. Seal cut edges. Do not print.')
 # Minimal DXF R12 entities in true mm, centered origin.
 ents=[]
 for a,b in [((-200,-200),(200,-200)),((200,-200),(200,200)),((200,200),(-200,200)),((-200,200),(-200,-200))]:ents.append(f'0\nLINE\n8\nOUTLINE\n10\n{a[0]}\n20\n{a[1]}\n11\n{b[0]}\n21\n{b[1]}\n')
 if name=='Upper_frame_plate':
  for x in [-70,70]:
   for y in [-65,65]:
    ps=[(x-14,y-2),(x+14,y-2),(x+14,y+2),(x-14,y+2)]
    for a,b in zip(ps,ps[1:]+ps[:1]):ents.append(f'0\nLINE\n8\nSTRAP_SLOTS\n10\n{a[0]}\n20\n{a[1]}\n11\n{b[0]}\n21\n{b[1]}\n')
 for x,y,r,_ in holes:ents.append(f'0\nCIRCLE\n8\nHOLES\n10\n{x:.5f}\n20\n{y:.5f}\n40\n{r}\n')
 open(OUT+'/Fabrication/'+name+'.dxf','w').write('0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n'+''.join(ents)+'0\nENDSEC\n0\nEOF\n')
 json.dump({'size_mm':[400,400,3],'holes':[dict(x=round(x,5),y=round(y,5),diameter=2*r,purpose=p) for x,y,r,p in holes]},open(OUT+'/Fabrication/'+name+'_holes.json','w'),indent=2)
for sx in [-1,1]:
 for sy in [-1,1]:
  a=math.atan2(sy,sx);direction=Vector((math.cos(a),math.sin(a),0))
  for r in [130,210]:
   for sign in [-1,1]:
    z=739+sign*10.6;q=cube((0,0,z),(30,54,20.8));hole(q,(0,0,739),15.05,60,'X')
    for u in [-8,8]:
     for v in [-21,21]:hole(q,(u,v,z),2.7,50)
    q.rotation_euler.z=a;q.location.x=direction.x*r;q.location.y=direction.y*r
    hard(q,f'MACHINED 6061 clamp r{r} {sx:+d} {sy:+d} half{sign:+d}',metal,'30 radial x54 tangential x42 assembled; 30.10 bore along radial axis, 0.4 split gap. 4 M5 through-bolts 16 x42 pattern. Trial torque/clamp slip and tube crush test required. NOT a printed part.')
   for u in [-8,8]:
    for v in [-21,21]:
     p=(r+u)*direction+Vector((-direction.y*v,direction.x*v,739));hard(cyl(p,2.5,56),'M5 frame through-bolt',metal)
  p0=direction*110;p1=direction*625;p0.z=p1.z=739;beam(f'30OD 27ID carbon arm {sx:+d} {sy:+d}',p0,p1,15,carbon,13.5)
  # Dimensions beyond published motor OD and prop span are clearance envelopes, not reverse-engineered purchased CAD.
  pc=direction*650;pc.z=760
  pod=hard(cube((direction.x*623,direction.y*623,739),(90,50,46)),f'X6 Plus G2 integrated pod {sx:+d} {sy:+d}',blue,'Approximate housing envelope. Manufacturer 30 mm tube interface. Adjust tube trim/insertion from actual pod to achieve 650 mm motor radius.');pod.rotation_euler.z=a
  hard(cyl(pc,34.45,32.9),f'X6 Plus G2 motor {sx:+d} {sy:+d}',metal,'68.9 mm nominal motor diameter; integrated unit incl prop/cable 748 g. Purchased unit, do not print.')
  hard(cyl((pc.x,pc.y,779),14,6),'Purchased propeller hub',orange)
  # Blade profile is schematic, actual swept diameter exactly 620 mm.
  for s in [-1,1]:
   coords=[(s*18,-12),(s*70,-27),(s*240,-25),(s*310,-7),(s*310,3),(s*230,15),(s*70,13),(s*18,9)]
   vs=[(x,y,z) for z in [-2,2] for x,y in coords];faces=[tuple(reversed(range(8))),tuple(range(8,16))]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)]
   me=bpy.data.meshes.new('Purchased blade envelope');me.from_pydata(vs,[],faces);me.update();o=bpy.data.objects.new(f'MFP24x8 blade {sx:+d} {sy:+d} {s:+d}',me);COL.objects.link(o);o.location=(pc.x,pc.y,786);o.rotation_euler.z=a+math.pi/2;hard(o,o.name,carbon,'Nonprintable visual blade; use genuine matched CW/CCW MFP24x8. 620 mm swept span.');o['Status']='PURCHASED PROP ENVELOPE'
# Custom welded tubular landing stand, lowered clear of the carbon motor arms.
for o in list(bpy.data.objects):
 if 'UNVERIFIED landing' in o.name or 'UNVERIFIED extended landing' in o.name:bpy.data.objects.remove(o,do_unlink=True)
col('15 • NONPRINT | stand, cover & interface references')
for sx in [-1,1]:
 for sy in [-1,1]:
  beam('UNVERIFIED landing outrigger',(sx*175,sy*130,680),(sx*260,sy*220,680),10,metal,8)
  beam('UNVERIFIED extended landing strut',(sx*260,sy*220,680),(sx*290,sy*245,40),10,metal,8)
  beam('UNVERIFIED landing saddle drop',(sx*175,sy*130,680),(sx*175,sy*130,709),10,metal,8)
  q=cube((sx*175,sy*130,712),(40,24,6))
  for dx in [-12,12]:hole(q,(sx*175+dx,sy*130,712),2.7,16)
  hard(q,'Landing saddle attachment plate',metal,'M5 pair to lower frame. 6061 tubular welded joint/gussets require fabrication fit-up and load test; CAD is not a weld procedure.')
 beam('UNVERIFIED landing skid',(sx*290,-300,30),(sx*290,300,30),12,metal,10)
col('02 • P2 battery and avionics | PURCHASE')
# Battery centered above load. Tray allows manufacturer +/-5 mm size tolerance.
hard(cube((0,0,766),(230,115,6)),'Battery anti-slip pad',black,'6 mm resilient pad; two independent 25 mm webbing straps around frame plate, longitudinal end restraint.')
hard(cube((0,0,828.5),(206,93,119)),'Tattu standard LiPo 12S 22Ah 30C',blue,'Manufacturer 206x93x119 +/-5 mm, 4650 +/-100 g; 44.4 V nominal, 50.4 V full. Custom power-tail termination pending supplier confirmation.')
for x in [-70,70]:
 for sy in [-1,1]:
  a=Vector((x,sy*65,760));b=Vector((x,sy*48,890));o=cube((a+b)/2,(25,2,(b-a).length));o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();hard(o,'Battery restraint webbing',orange)
 hard(cube((x,0,890),(25,98,2)),'Battery strap top',orange)
 hard(cube((x,0,758.5),(25,134,2)),'Battery strap below plate',orange)
# Electronics behind battery in plan; separate mounting foam and retainers are nonprinted.
hard(cube((0,120,777),(103.4,52.4,28)),'Holybro Pixhawk 6X with standard baseboard',black,'Envelope from official specification, strap/foam installation; connector access and actual board revision to verify.')
hard(cube((-125,0,779),(45,41,26)),'Holybro PM08 CAN tinned-wire',orange,'200 A published continuous, no stock XT90 bottleneck. 5.3 V flight controller outputs, CAN telemetry.')
hard(cube((125,0,772),(55,40.2,17.6)),'Hobbywing UBEC 25A HV',blue,'Set 7.4 V; power only servo supply harness. No 7.4 V to FC power input.')
hard(cube((65,125,768),(22,13,4)),'RadioMaster RP3 V2 ELRS receiver',blue,'5 V; CRSF UART. Dual antennas outside carbon shadow.')
beam('M10 GPS mast',(0,145,780),(0,145,980),4,metal)
hard(cyl((0,145,987.2),25,14.4),'Holybro M10 GPS with compass',blue,'GPS puck 50 x14.4 mm; raised from power wiring. Establish compass interference during test.')
for s in [-1,1]:beam('RP3 antenna reference',(s*155,135,770),(s*155,135,850),1.5,black)
# Labels and overview camera.
bpy.data.objects['PETAL DROP / P1'].data.body='PETAL DROP / P2'
cam=bpy.data.objects['ASSEMBLY • closed'];cam.location=(2300,-2900,1900);cam.rotation_euler=(Vector((0,0,530))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=2100
sc.camera=cam;sc.cycles.samples=24;sc.render.resolution_x=1800;sc.render.resolution_y=1400
for a in bpy.data.screens:
 for area in a.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_distance=2400;area.spaces.active.region_3d.view_location=(0,0,550)
# Machined-part mesh exports are explicitly segregated from printable STLs.
import struct
for o in list(bpy.data.objects):
 if o.name.startswith('MACHINED 6061 clamp'):
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.triangulate(bm,faces=list(bm.faces));fn=o.name.replace(' ','_')+'.stl'
  with open(OUT+'/Fabrication/'+fn,'wb') as f:
   f.write(b'MACHINE ALUMINIUM ONLY - MM'.ljust(80,b' '));f.write(struct.pack('<I',len(bm.faces)))
   for face in bm.faces:
    a,b,c=[v.co for v in face.verts];n=(b-a).cross(c-a).normalized();f.write(struct.pack('<12fH',*n,*a,*b,*c,0))
  bm.free()
json.dump(list(rows.values()),open(OUT+'/parts_manifest.json','w'),indent=2)
sc['Build_status']='P2 selected-component engineering prototype; physical fit/load/release/flight tests pending.'
sc['Petal_payload_target_kg']=1.;sc['Design_AUW_ceiling_kg']=21.;sc['Motor_diagonal_mm']=1300.
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/PetalDrop_1kg_Assembly.blend');print('P2_BUILD_SAVED',flush=True)
